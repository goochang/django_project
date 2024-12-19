from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Account(AbstractBaseUser):
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.user_id

    user_id = models.CharField(max_length=10)
    username = models.CharField(max_length=10, blank=True, default="")
    introduce = models.CharField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="images/profile/", blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        파일 이름이 user_id를 사용하도록 저장 전에 ID 설정
        """
        # ID가 없는 경우 먼저 저장하여 ID 생성
        if not self.id:
            super().save(*args, **kwargs)

        isFile = kwargs.pop("isFile", False)

        if isFile:
            # 파일 이름 다시 설정 - 파일 확장자 가져오기
            ext = self.photo.name.split(".")[-1]
            # 새 파일명: user_id.확장자
            self.photo.name = f"{self.id}.{ext}"
        super().save(*args, **kwargs)


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
