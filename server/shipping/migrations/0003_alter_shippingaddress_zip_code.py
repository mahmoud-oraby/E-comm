# Generated by Django 4.2.6 on 2023-11-21 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0002_alter_shippingaddress_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='zip_code',
            field=models.PositiveIntegerField(),
        ),
    ]