from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_author = models.BooleanField(default=False)

    @property
    def full_name(self):
        return self.get_full_name()