from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from store.forms import DiscountForm
from store.models import Discount


class DiscountListView(ListView):
    model = Discount
    template_name = "store/discount/discount_list.html"
    context_object_name = "discounts"


class DiscountCreateView(CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = "store/discount/discount_form.html"
    success_url = reverse_lazy("discount-list")


class DiscountUpdateView(UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = "store/discount/discount_form.html"
    success_url = reverse_lazy("discount-list")
