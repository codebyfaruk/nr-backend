import random
import string

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from store.forms import ProductAddForm, ProductEditForm
from store.models import Product


class ProductListView(TemplateView):
    template_name = "store/product/view_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context


class ProductAddView(CreateView):
    model = Product
    form_class = ProductAddForm
    template_name = "store/product/add_product.html"
    success_url = reverse_lazy("product")

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Logic for calculating selling price based on displayed price and discount
        if instance.displayed_price and instance.value:
            if instance.discount_type == "percent":
                discount = instance.displayed_price * (instance.value / 100)
            else:
                discount = instance.value
            instance.selling_price = instance.displayed_price - discount
            instance.discount_amount = discount
        else:
            instance.selling_price = instance.displayed_price or 0

        # Automatically generate barcode if not provided
        if not instance.short_name:
            instance.short_name = self.generate_short_name(instance.name)
        if not instance.barcode:
            instance.barcode = self.generate_barcode(instance.short_name)

        instance.save()
        return super().form_valid(form)

    def generate_barcode(self, short_name):
        # Ensure short_name is exactly 4 characters: pad or trim
        short = short_name.upper()[:4]
        if len(short) < 4:
            padding = "".join(random.choices(string.ascii_uppercase, k=4 - len(short)))
            short += padding

        prefix = "".join(random.choices(string.digits, k=4))
        suffix = "".join(random.choices(string.digits, k=4))

        return f"{prefix}{short}{suffix}"

    def generate_short_name(self, name):
        words = name.split()
        abbreviation = "".join(word[0] for word in words[:3]).upper()
        return abbreviation


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = "store/product/edit_product.html"

    def get_success_url(self):
        return reverse_lazy("product")

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Logic for calculating selling price based on displayed price and discount
        if instance.displayed_price and instance.value:
            if instance.discount_type == "percent":
                discount = instance.displayed_price * (instance.value / 100)
            else:
                discount = instance.value
            instance.selling_price = instance.displayed_price - discount
            instance.discount_amount = discount
        else:
            instance.selling_price = instance.displayed_price or 0

        if not instance.short_name:
            instance.short_name = self.generate_short_name(instance.name)

        instance.save()
        return super().form_valid(form)

    def generate_short_name(self, name):
        words = name.split()
        abbreviation = "".join(word[0] for word in words[:3]).upper()
        return abbreviation


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        """
        Override the get_queryset method to ensure we're only fetching a single product
        based on the provided product_id (URL parameter).
        """
        return Product.objects.filter(id=self.kwargs["pk"])
