from rest_framework import viewsets
from requirements.models import Requirement
from requirements.serializers import RequirementSerializer
from django.views.generic import TemplateView

class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer


class RequirementView(TemplateView):
    template_name = "requirement/index.html"
