from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import os
from accounts.utils import rename_imagefile_to_uid
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class OverwriteStorage(FileSystemStorage):
    """
    file 같은 이름 존재시 overwrite
    """

    def get_available_name(self, name, max_length=20):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Account(AbstractBaseUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    user_id = models.CharField(max_length=10)
    username = models.CharField(max_length=10, unique=True)
    introduce = models.CharField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        upload_to=rename_imagefile_to_uid, storage=OverwriteStorage(), blank=True
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)


class Follow(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="followers"
    )
    follow = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="following"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "follow"], name="unique_follow")
        ]
