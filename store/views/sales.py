from django.views.generic import TemplateView


class SalesView(TemplateView):
    template_name = "store/sales/sales.html"


class InvoiceView(TemplateView):
    template_name = "store/sales/invoice.html"
