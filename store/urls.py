from django.urls import path
from rest_framework.routers import DefaultRouter

from store.api_views import (
    CategoryViewSet,
    DiscountViewSet,
    InvoiceViewSet,
    ProductViewSet,
)
from store.views import DashboardView, ProductDetailView

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"discounts", DiscountViewSet, basename="discount")
router.register(r"invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("products/", ProductDetailView.as_view(), name="product"),
]
