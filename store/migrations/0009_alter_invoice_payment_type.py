# Generated by Django 5.2.1 on 2025-05-13 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_invoice_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('online', 'Online'), ('cash', 'Cash'), ('card', 'Card')], max_length=10, null=True),
        ),
    ]
