import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def select_for_update(self):
        raise NotImplementedError


class CustomUser(AbstractUser):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)

    objects = CustomUserManager()


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, swappable=True, on_delete=models.CASCADE
    )
