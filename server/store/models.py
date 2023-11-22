from django.db import models
from authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

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
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    size = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.size


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/images_product/')

    def __str__(self):
        return str(self.image)


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/images_product/')
    images = models.ManyToManyField(Image, blank=True, related_name="product")
    discount = models.PositiveIntegerField()
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="product")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product")
    colors = models.ManyToManyField(Color, blank=True, related_name="product")
    sizes = models.ManyToManyField(Size, blank=True, related_name="product")
    label = models.CharField(max_length=30, blank=True, null=True)
    available = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    free_shipping = models.BooleanField(default=False)
    selled = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Evaluation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user} - {self.product}"

# WishList model


class WishList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='wishlists')

    def __str__(self):
        return f'{self.user} wishlisted for {self.product}'

    # Class Meta
    class Meta:
        verbose_name_plural = "Wishlist"
        verbose_name = "Wishlist"
