from django.db import models
from authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)
    logo = models.ImageField(upload_to="uploads/logos_brand/")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=32)
    rgb = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Size(models.Model):
    size = models.CharField(max_length=10, unique=True, null=True)

    def __str__(self):
        return self.size


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="uploads/images_products/")
    discount = models.PositiveIntegerField()
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="product", null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product", null=True, blank=True)
    colors = models.ManyToManyField(Color, blank=True, related_name="product")
    sizes = models.ManyToManyField(Size, blank=True, related_name="product")
    available = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    free_shipping = models.BooleanField(default=False)
    selled = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Rate(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ratings")
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="ratings")
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user} rated {self.product} as {self.rate}"
