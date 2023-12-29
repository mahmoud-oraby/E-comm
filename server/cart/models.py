from django.db import models
from store.models import Product
from django.conf import settings
from django.db.models import Sum, F

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    coupon = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_cart_total(self):
        total = self.items.aggregate(
            cart_total=Sum(F('product__price')*F('quantity')))['cart_total']
        return total if total else 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="items")
    color = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.color and self.product.colors.exists():
            self.color = self.product.colors.first().name

        if not self.size and self.product.sizes.exists():
            self.size = self.product.sizes.first().size

        super().save(*args, **kwargs)

    def total_price(self):
        price = self.product.price * self.quantity
        return price

    def __str__(self):
        return f"{self.product} - {self.total_price()}"
