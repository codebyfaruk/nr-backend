# Generated by Django 5.2.1 on 2025-05-13 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_color_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='store.product'),
        ),
    ]
