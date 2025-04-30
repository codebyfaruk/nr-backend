from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from store.filters import ProductFilter
from store.models import Category, Discount, Invoice, Product
from store.permissions import IsStaffPermission
from store.serializers import (
    ApplyCouponSerializer,
    CategorySerializer,
    DiscountSerializer,
    InvoiceSerializer,
    ProductSerializer,
    SalesProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsStaffPermission]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffPermission]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
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


class ApplyCouponView(APIView):
    permission_classes = [IsStaffPermission]
    allow_staff = True

    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        total = serializer.validated_data["total"]
        user = request.user

        try:
            discount = Discount.objects.get(code__iexact=code)
        except Discount.DoesNotExist:
            return Response(
                {"detail": "Invalid coupon code."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not discount.is_valid_for(user, total):
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
