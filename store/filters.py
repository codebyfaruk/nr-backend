import django_filters

from store.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Product Name"
    )
    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains", label="Category"
    )
    barcode = django_filters.CharFilter(
        field_name="barcode", lookup_expr="icontains", label="Barcode"
    )
    cell_no = django_filters.CharFilter(
        field_name="cell_no", lookup_expr="icontains", label="Cell Number"
    )

    class Meta:
        model = Product
        fields = ["name", "category", "barcode", "cell_no"]
