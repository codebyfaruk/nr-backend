from django.views.generic import TemplateView


class CustomerListView(TemplateView):
    template_name = "store/customer/customer_list.html"
