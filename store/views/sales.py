from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from store.models import Invoice

class SalesView(TemplateView):
    template_name = "store/sales/sales.html"


class InvoiceView(TemplateView):
    template_name = "store/sales/invoice.html"

    def get_context_data(self, **kwargs):
        order_id = kwargs.get("pk")

        # Optimized query: fetch customer and prefetch related items
        order = get_object_or_404(
            Invoice.objects.select_related("customer").prefetch_related("items"),
            id=order_id
        )

        context = super().get_context_data(**kwargs)
        context["order"] = order
        context["items"] = order.items.all()
        return context
