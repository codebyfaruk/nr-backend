from django.views.generic import TemplateView

from store.models import Product
from store.utils.barcode_generator import generate_base64_barcode


class ProductLableView(TemplateView):
    template_name = "store/label/view_product.html"

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
    template_name = "store/label/print_labels.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ids = self.request.GET.get("ids", "")
        id_list = [int(i) for i in ids.split(",") if i.isdigit()]
        products = Product.objects.filter(id__in=id_list, is_active=True)

        for product in products:
            product.barcode_url = generate_base64_barcode(product.barcode)

        context["products"] = products
        return context
