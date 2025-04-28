from django.urls import path
from rest_framework.routers import DefaultRouter

from store.api_views import (
    CategoryViewSet,
    DiscountViewSet,
    InvoiceViewSet,
    ProductViewSet,
)
from store.views.dashboard import DashboardView
from store.views.product import (
    ProductAddView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="api_product")
router.register(r"categories", CategoryViewSet, basename="api_category")
router.register(r"discounts", DiscountViewSet, basename="api_discount")
router.register(r"invoices", InvoiceViewSet, basename="api_invoice")

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product"),
    path("product/add/", ProductAddView.as_view(), name="product_add"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
