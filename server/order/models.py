from django.db import models
from cart.models import Cart
from shipping.models import ShippingAddress
# Create your models here.


# Class Order
class Order(models.Model):
    STATUS_CHOICES = (('unpaid', 'unpaid'), ('pending', 'pending'), ('processing', 'processing'),
                      ('shipped', 'shipped'), ('delivered', 'delivered'), ('canceled', 'canceled'))
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    customer_name = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        decimal_places=2, max_digits=7, blank=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.SET_NULL, null=True, related_name="order")
    shipping = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True, related_name="order")
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=15, default='unpaid')

    def __str__(self):
        return f'{self.order_id}-{self.cart}'
