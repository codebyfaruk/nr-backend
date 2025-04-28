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
        if not instance.barcode:
            instance.barcode = self.generate_barcode()

        instance.save()  # Save the product instance
        return super().form_valid(form)

    def generate_barcode(self):
        # You can implement barcode generation logic here
        # For now, let's assume it's a random string (you can replace this with your barcode generation logic)
        import random

        return str(random.randint(100000, 999999))


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = "store/product/edit_product.html"

    def get_success_url(self):
        return reverse_lazy("product")

    def form_valid(self, form):
        return super().form_valid(form)


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
