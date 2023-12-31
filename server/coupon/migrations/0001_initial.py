# Generated by Django 4.2.6 on 2023-11-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30)),
                ('discount_type', models.CharField(choices=[('P', 'percentage'), ('F', 'fixed')], max_length=1)),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('limit', models.IntegerField()),
                ('redemption', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
