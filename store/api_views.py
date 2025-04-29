from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from store.filters import ProductFilter
from store.models import Category, Discount, Invoice, Product
from store.permissions import IsStaffPermission
from store.serializers import (
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
