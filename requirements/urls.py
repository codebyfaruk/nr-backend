from rest_framework.routers import DefaultRouter
from requirements.views import RequirementViewSet, RequirementView
from django.urls import path

router = DefaultRouter()
router.register(r'requirements', RequirementViewSet, basename='api_requirement')

urlpatterns = [
    path("", RequirementView.as_view(), name="requirement_view"),
]
