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


class Dashboard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Dashboard {self.name}'


class DashboardUser(models.Model):
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'DashboardUser {self.id}'


class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='join_requests')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Join Request {self.id}'


class Task(models.Model):
    TASK_STATES = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    state = models.CharField(max_length=10, choices=TASK_STATES, default='created')

    creator = models.ForeignKey(DashboardUser, on_delete=models.CASCADE, related_name='created_tasks')
    resolver = models.ForeignKey(DashboardUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_tasks')

    description = models.TextField()
    answer = models.TextField(blank=True)

    publication_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f'Task {self.id}'
