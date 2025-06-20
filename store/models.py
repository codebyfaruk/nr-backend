from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

from accounts.models import Customer

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Brand(TimeStampedModel, models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    bill_image = models.ImageField(upload_to="media/brand/", null=True, blank=True)
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


# Product model (for the clothing items)
class Product(TimeStampedModel, models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ("", "Select Discount Type"),
        ("flat", "Flat"),
        ("percent", "Percentage"),
    )

    name = models.CharField(max_length=255)
    short_name = models.CharField(
        max_length=100, null=True, blank=True
    )  # New short name field
    description = models.TextField(blank=True)
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Purchase price (₹100)
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Selling price (₹150)
    displayed_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Price shown to customer (₹200)
    discount_type = models.CharField(
        max_length=10, choices=DISCOUNT_TYPE_CHOICES, null=True, blank=True
    )
    value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # e.g. 10% or ₹100
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True, blank=True
    )  # Discount amount (₹50)
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="media/products/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_printed = models.BooleanField(default=False)
    barcode = models.CharField(max_length=255, unique=True)
    cell_no = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class Discount(TimeStampedModel, models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ("flat", "Flat"),
        ("percent", "Percentage"),
    )

    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=50, blank=True, null=True
    )  # For coupon-based discounts
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)  # e.g. 10% or ₹100
    max_discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Cap e.g. ₹500
    min_purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    applies_to_all = models.BooleanField(default=True)
    customers = models.ManyToManyField(
        Customer, blank=True
    )  # Only if applies_to_all=False
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def is_valid_for(self, customer, purchase_total):
        """Check if discount applies to a given customer and purchase total."""
        if not self.is_active:
            return False

        today = timezone.now().date()
        if self.start_date and self.start_date > today:
            return False
        if self.end_date and self.end_date < today:
            return False

        if not self.applies_to_all:
            if not customer or customer not in self.customers.all():
                return False

        if purchase_total < self.min_purchase_amount:
            return False

        return True

    def get_discount_amount(self, total):
        """Calculate discount amount"""
        if self.discount_type == "flat":
            discount = self.value
        else:
            discount = (self.value / 100) * total

        if self.max_discount_amount:
            return min(discount, self.max_discount_amount)
        return discount

    def __str__(self):
        return f"{self.name} ({'All' if self.applies_to_all else 'Specific'})"


# Invoice model (customer's purchase record)
class Invoice(TimeStampedModel, models.Model):
    INVOICE_STATUS_CHOICES = (
        ("draft", "Draft"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )
    PAYMENT_TYPE_CHOICES = (
        ('online', 'Online'),
        ('cash', 'Cash'),
        ('card', 'Card')
    )
    invoice_number = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=10, choices=INVOICE_STATUS_CHOICES, default="draft"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="invoices"
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Split discounts
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loyalty_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_date = models.DateTimeField(default=timezone.now)
    is_draft = models.BooleanField(default=True)

    payment_type = models.CharField(
        max_length=10, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True
    )

    @property
    def discount(self):
        return self.coupon_discount + self.loyalty_discount

    @property
    def amount_due(self):
        return max(self.total - self.amount_paid, 0)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer.name} ({self.status})"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    discount_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")

    @property
    def price_at_purchase(self):
        return self.rate - self.discount_at_purchase

    @property
    def total_price(self):
        return self.quantity * self.price_at_purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.short_name or self.product_name} (Invoice #{self.invoice.invoice_number})"
