from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    skin_type = models.JSONField(default=list, blank=True)
    skin_concerns = models.JSONField(default=list, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs) 