from rest_framework import viewsets
from requirements.models import Requirement
from requirements.serializers import RequirementSerializer
from django.views.generic import TemplateView
from store.models import Brand

class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer


class RequirementView(TemplateView):
    template_name = "requirement/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context