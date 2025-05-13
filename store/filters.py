import django_filters

from store.models import Product
from django.db.models import Sum, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from store.models import InvoiceItem
from django.db import models
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
    start_date = filters.DateTimeFilter(field_name="invoice__invoice_date", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="invoice__invoice_date", lookup_expr='lte')
    period = filters.ChoiceFilter(choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')], method='filter_by_period')

    class Meta:
        model = InvoiceItem
        fields = ['start_date', 'end_date', 'period']

    def filter_by_period(self, queryset, name, value):
        if value == 'day':
            return queryset.annotate(period=TruncDay('invoice__invoice_date')).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price'), output_field=models.DecimalField()),
                total_investment=Sum(F('product__purchase_price'), output_field=models.DecimalField())
            )
        elif value == 'week':
            return queryset.annotate(period=TruncWeek('invoice__invoice_date')).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price'), output_field=models.DecimalField()),
                total_investment=Sum(F('product__purchase_price'), output_field=models.DecimalField())
            )
        elif value == 'month':
            return queryset.annotate(period=TruncMonth('invoice__invoice_date')).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price'), output_field=models.DecimalField()),
                total_investment=Sum(F('product__purchase_price'), output_field=models.DecimalField())
            )
        elif value == 'year':
            return queryset.annotate(period=TruncYear('invoice__invoice_date')).values('period').annotate(
                total_profit=Sum(F('rate') - F('discount_at_purchase') - F('product__purchase_price'), output_field=models.DecimalField()),
                total_investment=Sum(F('product__purchase_price'), output_field=models.DecimalField())
            )
        return queryset

