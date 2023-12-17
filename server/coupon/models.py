from django.db import models

# Create your models here.


class Coupon(models.Model):
    DISCOUNT_TYPE = (
        ("P", "percentage"),
        ("F", "fixed"),
    )
    code = models.CharField(max_length=30)
    discount_type = models.CharField(choices=DISCOUNT_TYPE, max_length=1)
    discount_amount = models.DecimalField(decimal_places=2, max_digits=5)
    min_total = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    limit = models.IntegerField()
    redemption = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
