from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import CustomerView, CustomerViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="api_user")
router.register(r"customers", CustomerViewSet, basename="api_customer")

urlpatterns = [
    path("", CustomerView.as_view(), name="customer_view"),
]
