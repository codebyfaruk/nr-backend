from rest_framework import viewsets

from store.models import Category, Discount, Invoice, Product
from store.permissions import IsStaffPermission
from store.serializers import (
    CategorySerializer,
    DiscountSerializer,
    InvoiceSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffPermission]


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
