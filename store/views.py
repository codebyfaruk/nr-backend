from django.views.generic import TemplateView

from store.models import Product


class DashboardView(TemplateView):
    template_name = "index.html"


class ProductDetailView(TemplateView):
    template_name = "store/product/view_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context
