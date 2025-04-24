from django.core.management.base import BaseCommand

from store.factories import (
    CategoryFactory,
    CustomerFactory,
    DiscountFactory,
    InvoiceFactory,
    InvoiceItemFactory,
    ProductFactory,
)


class Command(BaseCommand):
    help = "Populate the database with dummy data for testing"

    def handle(self, *args, **kwargs):
        # Create dummy data using factories
        CustomerFactory.create_batch(5)  # Create 5 users (customers)
        CategoryFactory.create_batch(10)  # Create 10 products
        ProductFactory.create_batch(10)  # Create 10 products
        DiscountFactory.create_batch(3)  # Create 10 products
        invoices = InvoiceFactory.create_batch(3)  # Create 3 invoices

        # Create invoice items for each invoice
        for invoice in invoices:
            InvoiceItemFactory.create_batch(2, invoice=invoice)  # 2 items per invoice

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with test data")
        )
