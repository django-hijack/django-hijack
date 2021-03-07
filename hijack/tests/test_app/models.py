import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
