from django.db import models
from store.models import Product
from django.conf import settings

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        price = self.product.price * self.quantity
        return price

    def __str__(self):
        return f"{self.product} - {self.total_price()}"
