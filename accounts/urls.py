from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

# Expose only the router’s URLs
urlpatterns = [
    path("", include(router.urls)),
]
