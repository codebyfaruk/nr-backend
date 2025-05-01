from django import forms

from store.models import Category, Discount, Product


class ProductAddForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    discount_type = forms.ChoiceField(
        required=False,
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
            "color",
            "size",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control select2",
                    "placeholder": "Enter product name",
                    "required": "required",
                }
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
            "color": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color"}
            ),
            "size": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Size"}
            ),
        }


class ProductEditForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    discount_type = forms.ChoiceField(
        required=False,
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
            "is_active",
            "size",
            "color",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name",
                    "required": "required",
                }
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
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "color": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Color"}
            ),
            "size": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Size"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].label = ""


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
