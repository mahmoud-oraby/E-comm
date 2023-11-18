from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
# Create your models here.


class ShippingAddress(models.Model):
    user = models.CharField(max_length=30, blank=True, unique=True)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16,  blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    zip_code = models.PositiveIntegerField(
        validators=[MinLengthValidator(3), MaxLengthValidator(8)])
    primary_address = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.user} - {str(self.address1)}"
