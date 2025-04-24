import random
import string

from rest_framework import serializers

from accounts.models import CustomUser
from store.models import Category, Discount, Invoice, InvoiceItem, Product


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
            "category",  # Readable nested info
            "category_id",  # ID input for create/update
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

    def generate_barcode(self, short_name):
        prefix = "".join(random.choices(string.digits, k=4))
        suffix = "".join(random.choices(string.digits, k=6))
        return f"{prefix}{short_name[:4].upper()}{suffix}".upper()

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
        validated_data["barcode"] = self.generate_barcode(short_name)

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


class InvoiceItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = InvoiceItem
        fields = ["id", "product", "quantity", "price_at_purchase", "total_price"]


class InvoiceSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    items = InvoiceItemSerializer(many=True)
    amount_due = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "customer",
            "items",
            "subtotal",
            "product_discount",
            "coupon_discount",
            "loyalty_discount",
            "total",
            "amount_paid",
            "amount_due",
            "invoice_date",
        ]

    def get_amount_due(self, obj):
        return obj.amount_due

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice
