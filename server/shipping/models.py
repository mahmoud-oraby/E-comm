from django.db import models
from django.core.validators import MaxValueValidator, MaxLengthValidator
# Create your models here.


class ShippingAddress(models.Model):
    user = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16,  blank=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=16)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    zip_code = models.PositiveIntegerField()
    primary_address = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.user} - {str(self.address1)}"
