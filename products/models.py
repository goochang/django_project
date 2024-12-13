from django.db import models
from accounts.models import Account
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=10)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    price = models.IntegerField(default=0)
    type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="images/", blank=True)


# class ProductImage(models.Model):
#     image_name = models.CharField(max_length=10)
#     product_image = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
