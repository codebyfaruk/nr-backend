from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, DiscountViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"products", ProductViewSet)
router.register(r"discounts", DiscountViewSet)
