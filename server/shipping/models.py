from django.db import models
# Create your models here.


class ShippingAddress(models.Model):
    user = models.CharField(max_length=30, blank=True, unique=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    state = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user} - {str(self.address1)}"
