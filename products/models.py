from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=10)
    price = models.IntegerField(default=0)
    type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductImage(models.Model):
    image_name = models.CharField(max_length=10)
    product_image = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)