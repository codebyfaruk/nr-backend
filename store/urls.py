from rest_framework.routers import DefaultRouter

from store.views import CategoryViewSet, DiscountViewSet, InvoiceViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"discounts", DiscountViewSet, basename="discount")
router.register(r"invoices", InvoiceViewSet, basename="invoice")
