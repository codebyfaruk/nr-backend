from rest_framework.routers import DefaultRouter

from accounts.views import CustomerViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"customers", CustomerViewSet, basename="customer")
