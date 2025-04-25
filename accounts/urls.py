from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import CustomerView, CustomerViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = [
    path("", CustomerView.as_view(), name="customer_view"),
]
