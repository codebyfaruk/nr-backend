import django_filters

from store.models import Product
from django.db.models import Sum, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from store.models import InvoiceItem
from django.utils.timezone import now
from datetime import timedelta
from django_filters import rest_framework as filters


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

# Define a filter class to handle the filtering by date range
class SalesProfitFilter(filters.FilterSet):
    period = filters.ChoiceFilter(
        choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')],
        method='filter_by_period'
    )

    class Meta:
        model = InvoiceItem
        fields = ['period']

    def filter_by_period(self, queryset, name, value):
        queryset = queryset.filter(invoice__is_draft=False)

        today = now().date()

        if value == 'day':
            return queryset.filter(invoice__invoice_date__date=today).annotate(
                period=TruncDay('invoice__invoice_date')
            ).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price')),
                total_investment=Sum(F('product__purchase_price'))
            )

        elif value == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            return queryset.filter(invoice__invoice_date__date__gte=start_of_week).annotate(
                period=TruncWeek('invoice__invoice_date')
            ).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price')),
                total_investment=Sum(F('product__purchase_price'))
            )

        elif value == 'month':
            return queryset.filter(invoice__invoice_date__month=today.month, invoice__invoice_date__year=today.year).annotate(
                period=TruncMonth('invoice__invoice_date')
            ).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price')),
                total_investment=Sum(F('product__purchase_price'))
            )

        elif value == 'year':
            return queryset.filter(invoice__invoice_date__year=today.year).annotate(
                period=TruncYear('invoice__invoice_date')
            ).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price')),
                total_investment=Sum(F('product__purchase_price'))
            )

        return queryset