from rest_framework import viewsets
from labels.models import LabelTemplate
from labels.serializers import LabelTemplateSerializer
from django.views.generic import TemplateView
from store.models import Product
from labels.utils.barcode_generator import generate_base64_barcode
from django.shortcuts import get_object_or_404

class LabelTemplateViewSet(viewsets.ModelViewSet):
    queryset = LabelTemplate.objects.all()
    serializer_class = LabelTemplateSerializer

    def perform_create(self, serializer):
        # If 'is_default' is set to True, unset it for all others
        print(self.request.data.get('is_default'))
        if self.request.data.get('is_default') in ['true', 'True', True, '1', 1]:
            LabelTemplate.objects.filter(is_default=True).update(is_default=False)
        serializer.save()

class ProductLableView(TemplateView):
    template_name = "label/view_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = (
            Product.objects.filter(is_active=True)
            .values(
                "id",
                "name",
                "selling_price",
                "displayed_price",
                "stock_quantity",
                "is_printed",
                "barcode",
                "cell_no",
            )
            .order_by("is_printed")
        )
        return context


class PrintLabelView(TemplateView):
    template_name = "label/print_labels_new.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template_id = self.request.GET.get("template_id")
        ids = self.request.GET.get("ids", "")
        id_list = [int(i) for i in ids.split(",") if i.isdigit()]
        products = Product.objects.filter(id__in=id_list, is_active=True)
        template = get_object_or_404(LabelTemplate, id=template_id)

        for product in products:
            product.barcode_url = generate_base64_barcode(product.barcode)

        context["products"] = products
        context['template'] = template
        return context

