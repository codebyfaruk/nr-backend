from django.urls import path
from rest_framework.routers import DefaultRouter

from store.api_views import (
    CategoryViewSet,
    DiscountViewSet,
    InvoiceViewSet,
    ProductViewSet,
    SalesProductViewSet,
    SalesProfitViewSet,
    BrandViewSet,
)
from store.views.customer import CustomerListView
from store.views.dashboard import DashboardView
from store.views.discount import (
    DiscountCreateView,
    DiscountListView,
    DiscountUpdateView,
)
from store.views.product import (
    ProductAddView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)
from store.views.sales import InvoiceListView, InvoiceView, SalesView

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="api_product")
router.register(r"categories", CategoryViewSet, basename="api_category")
router.register(r"discounts", DiscountViewSet, basename="api_discount")
router.register(r"invoices", InvoiceViewSet, basename="api_invoice")
router.register(r"sales-product", SalesProductViewSet, basename="api_sales_product")
router.register(r'sales-profit', SalesProfitViewSet, basename='sales_profit')
router.register(r'brands', BrandViewSet, basename="api_brand")

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product"),
    path("product/add/", ProductAddView.as_view(), name="product_add"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("sales/", SalesView.as_view(), name="sales"),
    path("invoice/<int:pk>/", InvoiceView.as_view(), name="invoice"),
    path("invoice-list/", InvoiceListView.as_view(), name="invoice-list"),
    path("coupons/", DiscountListView.as_view(), name="discount-list"),
    path("coupons/add/", DiscountCreateView.as_view(), name="discount-add"),
    path("coupons/<int:pk>/edit/", DiscountUpdateView.as_view(), name="discount-edit"),
    path("customers/", CustomerListView.as_view(), name="customer_list"),
]
