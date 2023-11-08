# Generated by Django 4.2.6 on 2023-10-16 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_color_product_colors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, related_name='product', to='store.color'),
        ),
    ]