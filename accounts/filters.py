import django_filters

from accounts.models import Customer


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Customer Name"
    )
    phone = django_filters.CharFilter(
        field_name="phone", lookup_expr="icontains", label="Phone"
    )
    address = django_filters.CharFilter(
        field_name="address", lookup_expr="icontains", label="Address"
    )

    class Meta:
        model = Customer
        fields = ["name", "phone", "address"]
