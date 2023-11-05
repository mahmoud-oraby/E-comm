from django.db import models
from cart.models import Cart
# Create your models here.


# Class Order
class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    customer_name = models.CharField(max_length=100, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.SET_NULL, null=True, related_name="order")

    def __str__(self):
        return self.order_id
