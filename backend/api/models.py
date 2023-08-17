from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
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
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Dashboard {self.title}'


class DashboardUser(models.Model):
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    last_activity = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'DashboardUser {self.id}'


class JoinRequest(models.Model):
    REQUEST_STATES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=10, choices=REQUEST_STATES, default='pending')

    def __str__(self):
        return f'Join Request {self.id}'


class Task(models.Model):
    TASK_STATES = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    state = models.CharField(max_length=10, choices=TASK_STATES, default='created')

    creator = models.ForeignKey(DashboardUser, on_delete=models.CASCADE)
    resolver = models.ForeignKey(DashboardUser, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.TextField(max_length=45)
    description = models.TextField()
    answer = models.TextField(blank=True)

    publication_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f'Task {self.id}'


@receiver([post_save, post_delete], sender=Task)
def update_last_activity_for_task(sender, instance, **kwargs):
    dashboard_user = instance.creator
    dashboard_user.last_activity = timezone.now()
    dashboard_user.save()
