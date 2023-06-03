from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    subscription    = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)
    