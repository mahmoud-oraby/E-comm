from django.db import models
from order.models import Order
# Create your models here.

# Shipping Address


class ShippingAddress(models.Model):
    user = models.CharField(max_length=30)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="shipping")
    address1 = models.CharField(max_length=250, blank=True)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250, blank=True)
    zipcode = models.IntegerField()
    country = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.user} - {str(self.address1)}"
