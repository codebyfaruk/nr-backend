from django.urls import path
from rest_framework.routers import DefaultRouter
from labels.views import LabelTemplateViewSet
from labels.views import PrintLabelView, ProductLableView, LabelTemplateListView, LabelTemplateUpdateView
router = DefaultRouter()
router.register(r'labels', LabelTemplateViewSet, basename='api_labels')

urlpatterns = [
    path("labels/", ProductLableView.as_view(), name="labels"),
    path("products/print-labels/", PrintLabelView.as_view(), name="print_labels"),
    path('templates/', LabelTemplateListView.as_view(), name='label_template_list'),
    path('templates/<int:pk>/edit/', LabelTemplateUpdateView.as_view(), name='label_template_edit'),
]
