from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('HR', 'HR'),
        ('INTERVIEWER', 'INTERVIEWER'),
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)

    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='HR')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name']

    def __str__(self):
        return self.email