from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from datetime import datetime, timezone


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=45, null=True)
    username = models.CharField(max_length=45, null=False)
    last_name = models.CharField(max_length=45, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email

    def save_last_login(self):
        self.last_login = datetime.now()
        self.save()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):

        return self.username
