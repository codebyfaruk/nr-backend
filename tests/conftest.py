import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from accounts.models import Customer
from store.models import Category, Product, Discount, Invoice, InvoiceItem

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        if 'password' not in kwargs:
            kwargs['password'] = 'testpass123'
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def admin_user(api_client, create_user):
    user = create_user(username="testuser", is_admin=True)
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def staff_user(api_client, create_user):
    user = create_user(username="testuser", is_admin=False, is_staff=True)
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def super_user(api_client, create_user):
    user = create_user(username="testuser", is_admin=True, is_staff=True, is_superuser=True)
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def customer(db):
    return Customer.objects.create(
        name="John Doe", email="john@example.com", phone="1234567890"
    )

@pytest.fixture
def category(db):
    return Category.objects.create(name="T-Shirts")

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Basic T-Shirt",
        purchase_price=100,
        selling_price=150,
        displayed_price=200,
        stock_quantity=50,
        category=category,
        barcode="123456789012",
    )

@pytest.fixture
def discount(db):
    return Discount.objects.create(
        name="New Year Sale",
        discount_type="percent",
        value=10,
        is_active=True,
        applies_to_all=True
    )

@pytest.fixture
def invoice(db, customer):
    return Invoice.objects.create(
        invoice_number="INV1001",
        customer=customer,
        subtotal=500,
        coupon_discount=50,
        loyalty_discount=20,
        total=430,
        amount_paid=430,
        is_draft=False,
    )

@pytest.fixture
def invoice_item(db, invoice, product):
    return InvoiceItem.objects.create(
        invoice=invoice,
        product_name=product.name,
        quantity=2,
        rate=150,
        discount_at_purchase=10,
        product=product
    )
