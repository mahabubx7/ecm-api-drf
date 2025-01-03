from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import BaseModel

class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-created_at'] 