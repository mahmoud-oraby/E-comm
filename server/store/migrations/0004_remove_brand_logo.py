# Generated by Django 4.2.6 on 2023-11-14 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_brand_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='logo',
        ),
    ]
