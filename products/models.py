from django.db import models
from accounts.models import Account
from django.conf import settings

from products.utils import OverwriteStorage, rename_imagefile_to_pid


class Product(models.Model):
    name = models.CharField(max_length=10)
    viewCnt = models.IntegerField(default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        upload_to=rename_imagefile_to_pid, storage=OverwriteStorage()
    )


class Wish(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_id", "user_id"], name="unique_wish"
            )
        ]


# class ProductImage(models.Model):
#     image_name = models.CharField(max_length=10)
#     product_image = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
