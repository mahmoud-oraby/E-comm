# Generated by Django 4.2.6 on 2023-11-24 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0004_alter_shippingaddress_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='primary_address',
            new_name='default_address',
        ),
    ]
