from django.db import models
from store.models import Product
from django.conf import settings

# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, related_name='wish',
                                 on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wish")

    def __str__(self):
        return f"{self.product}"
