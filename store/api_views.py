from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import uuid
from accounts.models import Customer
from store.filters import ProductFilter, SalesProfitFilter
from store.models import Category, Discount, Invoice, Product, InvoiceItem
from store.permissions import IsStaffPermission
from store.serializers import (
    ApplyCouponSerializer,
    CategorySerializer,
    DiscountSerializer,
    InvoiceSerializer,
    ProductSerializer,
    SalesProductSerializer,
)
from decimal import Decimal
from accounts.serializers import CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter

    @action(detail=True, methods=["post"], url_path="check-discount")
    def check_discount(self, request, pk=None):
        try:
            product = self.get_object()
            purchase_price = float(product.purchase_price)
            discount_amount = float(request.data.get("discount_amount", 0))
            min_allowed_price = purchase_price * 1.10

            discounted_price = float(product.displayed_price) - discount_amount

            if discounted_price < min_allowed_price:
                return Response(
                    {"error": "You can't sell this product at this amount."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response({"message": "Discount is valid."})

        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid discounted price."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsStaffPermission]

    @action(detail=False, methods=["POST"], url_path="apply")
    def apply(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        total = serializer.validated_data["total"]
        customer_id = serializer.validated_data.get("customer_id")

        try:
            discount = Discount.objects.get(code__iexact=code)
        except Discount.DoesNotExist:
            return Response(
                {"detail": "Invalid coupon code."}, status=status.HTTP_400_BAD_REQUEST
            )
        customer = None
        if customer_id:
            customer = Customer.objects.filter(id=customer_id).first()

        if not discount.is_valid_for(customer, total):
            return Response(
                {"detail": "This coupon is not valid for you or your purchase."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        discount_amount = discount.get_discount_amount(total)
        return Response(
            {
                "original_total": total,
                "discount": discount_amount,
                "final_total": total - discount_amount,
                "discount_name": discount.name,
            }
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffPermission]

class SalesProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True, stock_quantity__gt=0)
    serializer_class = SalesProductSerializer
    permission_classes = [IsStaffPermission]
    allow_staff = True
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if queryset.count() == 1:
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
    
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().prefetch_related('items', 'customer')
    serializer_class = InvoiceSerializer
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        payload = request.data
        customer_id = payload.get("customerId")
        products = payload.get("products", [])
        coupon = payload.get("coupon", {})
        coupon_amount = float(coupon.get("couponAmount") or 0)
        loyalty_discount = float(payload.get("roundoff") or 0)
        amount_paid = float(payload.get("paidAmount") or 0)
        payment_type = payload.get("paymentType")

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        subtotal = sum(float((p['rate'])- float(p['discount'])) * p['qty'] for p in products)

        if (amount_paid > 0):
            amount_paid = amount_paid
            is_draft = False
            paid_status = 'paid'
        else:
            amount_paid = 0
            is_draft = True
            paid_status = 'draft'
        
        invoice = Invoice.objects.create(
            invoice_number="INV-"+str(uuid.uuid4().int)[:8],
            customer=customer,
            subtotal=subtotal,
            coupon_discount=coupon_amount,
            loyalty_discount=loyalty_discount,
            total=subtotal - (coupon_amount+loyalty_discount),
            amount_paid= amount_paid,
            status=paid_status,
            is_draft=is_draft,
            payment_type = payment_type,

        )

        for item in products:
            try:
                product = Product.objects.get(id=item['id'])
                product.stock_quantity = product.stock_quantity - int(item['qty'])
                product.save()
            except Exception as e:
                print(e)
                product = None
            
            InvoiceItem.objects.create(
                invoice=invoice,
                product_name=item['productName'],
                quantity=item['qty'],
                rate=item['rate'],
                discount_at_purchase=item['discount'],
                product=product 
            )

        serializer = self.get_serializer(invoice)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', True)
        data = request.data

        # Extract and update customer
        customer_id = data.get("customerId")
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update customer fields
        customer.name = data.get("customerName", customer.name)
        customer.phone = data.get("customerPhone", customer.phone)
        customer.address = data.get("customerAddress", customer.address)
        customer.save()

        # Update invoice fields
        amount_paid = Decimal(data.get("paidAmount") or 0)
        payment_type = data.get("paymentType") or None
        payment_status = data.get("invoiceStatus") or None

        # Pass customer ID (not object) and other fields as primitives
        update_data = {
            "amount_paid": amount_paid,
            "payment_type": payment_type,
            "status": payment_status
        }

        serializer = self.get_serializer(instance, data=update_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return the full serialized data of the updated invoice
        full_serializer = self.get_serializer(instance)
        return Response(full_serializer.data)


    
    @action(detail=False, methods=['get'], url_name='customer-details')
    def get_customer_with_draft(self, request):
        phone = request.query_params.get('phone')
        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        draft_invoice = Invoice.objects.filter(customer=customer, is_draft=True).prefetch_related('items').first()

        customer_data = CustomerSerializer(customer).data
        invoice_data = InvoiceSerializer(draft_invoice).data if draft_invoice else None

        return Response({
            "customer": customer_data,
            "draft_invoice": invoice_data
        }, status=status.HTTP_200_OK)
    
class SalesProfitViewSet(viewsets.ViewSet):
    def list(self, request):
        # Apply filter based on the query params (start_date, end_date, period)
        queryset = InvoiceItem.objects.all()
        filtered_queryset = SalesProfitFilter(request.query_params, queryset=queryset).qs
        
        # Prepare the response data
        data = []
        for item in filtered_queryset:
            data.append({
                'period': item['period'],
                'total_profit': item['total_profit'] or 0,
                'total_investment': item['total_investment'] or 0,
            })

        return Response(data)