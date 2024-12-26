from django.db import models
from accounts.models import Account
from django.conf import settings

from products.utils import OverwriteStorage, rename_imagefile_to_pid


class HashTag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


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
    hashtags = models.ManyToManyField(
        HashTag, through="ProductHashtag", related_name="products"
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
            models.UniqueConstraint(fields=["product", "user"], name="unique_wish")
        ]


class ProductHashtag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "hashtag"], name="unique_product_hashtag"
            )
        ]


# class ProductImage(models.Model):
#     image_name = models.CharField(max_length=10)
#     product_image = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
