# Generated by Django 4.2.6 on 2023-12-20 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_wishlistitem_added_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlistitem',
            old_name='added_date',
            new_name='created_at',
        ),
    ]
