from django.db import models

# Create your models here.


class PaymentDetails(models.Model):
    order_id = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    last_digits = models.SmallIntegerField()

    def __str__(self):
        return self.name
