import random
import string

from rest_framework import serializers

from accounts.models import CustomUser
from store.models import Category, Discount, Invoice, InvoiceItem, Product
from accounts.serializers import CustomerSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "short_name",
            "description",
            "purchase_price",
            "selling_price",
            "displayed_price",
            "discount_type",
            "value",
            "discount_amount",
            "stock_quantity",
            "category",
            "category_id",
            "brand",
            "image",
            "is_active",
            "barcode",
            "cell_no",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "short_name",
            "barcode",
            "discount_amount",
            "created_at",
            "updated_at",
            "is_active",
        ]

    def get_short_name(self, name):
        words = name.split()
        abbreviation = "".join(word[0] for word in words[:3]).upper()
        return abbreviation

    def create(self, validated_data):
        # Generate short name from product name
        name = validated_data.get("name")
        short_name = self.get_short_name(name)
        validated_data["short_name"] = short_name

        # Generate barcode
        validated_data["barcode"] = random.choices(string.digits, k=12)

        # Calculate discount amount if applicable
        value = validated_data.get("value")
        discount_type = validated_data.get("discount_type")
        displayed_price = validated_data.get("displayed_price", 0)

        if discount_type and value:
            if discount_type == "flat":
                validated_data["discount_amount"] = value
            elif discount_type == "percent":
                validated_data["discount_amount"] = (value / 100) * displayed_price
        else:
            validated_data["discount_amount"] = 0

        return super().create(validated_data)


class DiscountSerializer(serializers.ModelSerializer):
    customers = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True
    )

    class Meta:
        model = Discount
        fields = "__all__"


# InvoiceItem Serializer
class InvoiceItemSerializer(serializers.ModelSerializer):
    price_at_purchase = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = [
            "id",
            "product_name",
            "quantity",
            "rate",
            "discount_at_purchase",
            "price_at_purchase",
            "total_price",
        ]


# Invoice Serializer
class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    items = InvoiceItemSerializer(many=True)  # Nested items
    discount = serializers.ReadOnlyField()  # Computed discount field
    amount_due = serializers.ReadOnlyField()  # Computed amount_due field

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "status",
            "customer",
            "subtotal",
            "coupon_discount",
            "loyalty_discount",
            "total",
            "amount_paid",
            "invoice_date",
            "is_draft",
            "discount",
            "amount_due",
            "items",
            "payment_type",
        ]

    # You may want to override the create and update methods if you need specific logic.
    def create(self, validated_data):
        # Custom create logic if needed
        items_data = validated_data.pop("items", [])
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def update(self, instance, validated_data):
        # Custom update logic if needed
        items_data = validated_data.pop("items", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update items (if provided in the request)
        for item_data in items_data:
            item_id = item_data.get("id")
            if item_id:
                item = InvoiceItem.objects.get(id=item_id, invoice=instance)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                InvoiceItem.objects.create(invoice=instance, **item_data)
        return instance


class SalesProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "selling_price",
            "displayed_price",
            "discount_type",
            "value",
            "discount_amount",
            "stock_quantity",
            "barcode",
        ]


class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    cutomer_id = serializers.IntegerField(required=False, allow_null=True)
