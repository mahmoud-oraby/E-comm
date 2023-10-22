# Generated by Django 4.2.6 on 2023-10-22 20:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_product_rate_num_product_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.DeleteModel(
            name='Rate',
        ),
    ]
