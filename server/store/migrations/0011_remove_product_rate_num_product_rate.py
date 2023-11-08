# Generated by Django 4.2.6 on 2023-10-22 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_rename_rate_product_rate_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rate_num',
        ),
        migrations.AddField(
            model_name='product',
            name='rate',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]