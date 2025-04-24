# invoices/factories.py
import random
from decimal import Decimal

import factory
from django.utils import timezone
from faker import Faker

from accounts.models import Customer
from store.models import Category, Discount, Invoice, InvoiceItem, Product

fake = Faker()


# Factory for Customer
class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    email = factory.Faker("email")
    phone = factory.LazyFunction(lambda: fake.phone_number()[:15])
    name = factory.Faker("name")
    address = factory.Faker("address")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")

    @factory.lazy_attribute
    def parent(self):
        # Randomly assign parent 50% of the time if categories exist
        if Category.objects.exists() and random.choice([True, False]):
            return random.choice(Category.objects.all())
        return None


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    short_name = factory.Faker("word")
    description = factory.Faker("sentence")
    purchase_price = factory.LazyAttribute(lambda x: Decimal("100.00"))
    selling_price = factory.LazyAttribute(lambda x: Decimal("150.00"))
    displayed_price = factory.LazyAttribute(lambda x: Decimal("200.00"))
    discount_amount = factory.LazyAttribute(lambda x: Decimal("50.00"))
    stock_quantity = factory.LazyAttribute(lambda x: 100)
    category = factory.SubFactory(CategoryFactory)
    brand = factory.Faker("company")
    image = factory.Faker("image_url")
    is_active = factory.LazyAttribute(lambda x: True)
    barcode = factory.Faker("ean13")
    cell_no = factory.Faker("random_number", digits=5)


class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount

    name = factory.Faker("word")
    code = factory.Faker("word")
    discount_type = factory.Faker("random_element", elements=["flat", "percent"])
    value = factory.LazyAttribute(lambda x: Decimal("10.00"))
    max_discount_amount = factory.LazyAttribute(lambda x: Decimal("500.00"))
    min_purchase_amount = factory.LazyAttribute(lambda x: Decimal("2000.00"))
    applies_to_all = factory.LazyAttribute(lambda x: True)
    start_date = factory.LazyFunction(lambda: timezone.now())
    end_date = factory.LazyAttribute(
        lambda x: timezone.now() + timezone.timedelta(days=10)
    )
    is_active = factory.LazyAttribute(lambda x: True)


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    customer = factory.SubFactory(CustomerFactory)  # Link to Customer
    subtotal = factory.LazyAttribute(lambda x: Decimal("1000.00"))
    product_discount = factory.LazyAttribute(lambda x: Decimal("50.00"))
    coupon_discount = factory.LazyAttribute(lambda x: Decimal("20.00"))
    loyalty_discount = factory.LazyAttribute(lambda x: Decimal("30.00"))
    total = factory.LazyAttribute(lambda x: Decimal("900.00"))
    amount_paid = factory.LazyAttribute(lambda x: Decimal("900.00"))
    invoice_date = factory.LazyFunction(lambda: timezone.now())


class InvoiceItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InvoiceItem

    invoice = factory.SubFactory(InvoiceFactory)  # Link to Invoice
    product = factory.SubFactory(ProductFactory)  # Link to Product
    quantity = factory.LazyAttribute(lambda x: 2)  # Quantity example
    price_at_purchase = factory.LazyAttribute(lambda x: Decimal("150.00"))
