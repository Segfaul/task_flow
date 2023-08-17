from django.core.exceptions import ValidationError

from .models import Task


def validate_user(data):
    username = data['username'].strip()
    password = data['password'].strip()

    if not password or len(password) < 8:
        raise ValidationError('password is incorrectly set (minimum 8 characters)')

    if (not username) or (len(username) >= 150):
        raise ValidationError('choose another username')

    return data


def validate_task(instance, data):
    dashboard_id = data['dashboard']
    title = data['title']

    duplicate = Task.objects.filter(dashboard_id=dashboard_id, title=title).exclude(id=instance.id if instance else None).first()

    if duplicate:
        raise ValidationError('Task with the same title already exists in dashboard')

    return data
