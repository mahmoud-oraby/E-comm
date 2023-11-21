from django.db import models

# Create your models here.


class Message(models.Model):
    full_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=255)
    message = models.TextField()
