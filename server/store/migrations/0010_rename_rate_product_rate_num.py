# Generated by Django 4.2.6 on 2023-10-22 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='rate',
            new_name='rate_num',
        ),
    ]
