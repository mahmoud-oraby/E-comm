# Generated by Django 4.2.6 on 2023-11-24 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_image_image_alter_product_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WishList',
        ),
    ]