from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_superuser = False):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        return self.create_user(username, password, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150)
    api_token = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class Task(models.Model):
    TASK_STATUSES = (
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    )
    task_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
