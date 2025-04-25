from django import forms

from store.models import Category, Product


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    discount_type = forms.ChoiceField(
        choices=Product.DISCOUNT_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "short_name",
            "description",
            "purchase_price",
            "category",
            "cell_no",
            "displayed_price",
            "discount_type",
            "value",
            "stock_quantity",
            "brand",
            "image",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter product name"}
            ),
            "short_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter short name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product description",
                    "rows": 4,
                }
            ),
            "purchase_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter purchase price"}
            ),
            "cell_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter cell number"}
            ),
            "displayed_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Displayed price"}
            ),
            "value": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Discount value"}
            ),
            "stock_quantity": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Stock quantity"}
            ),
            "brand": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Brand name"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
