# Generated by Django 4.2.6 on 2023-10-14 21:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_brand_rateproduct_product_brand'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RateProduct',
            new_name='Rate',
        ),
    ]
