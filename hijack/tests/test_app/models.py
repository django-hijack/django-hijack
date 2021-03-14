import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, swappable=True, on_delete=models.CASCADE
    )
