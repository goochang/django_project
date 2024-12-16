from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Account(AbstractBaseUser):
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_id

    user_id = models.CharField(max_length=10)
    username = models.CharField(max_length=10, null=True)
    # password = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="images/profile/", blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
