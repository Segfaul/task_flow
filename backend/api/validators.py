from django.core.exceptions import ValidationError


def validate_user(data):
    username = data['username'].strip()
    password = data['password'].strip()

    if not password or len(password) < 8:
        raise ValidationError('password is incorrectly set (minimum 8 characters)')

    if (not username) or (len(username) >= 150):
        raise ValidationError('choose another username')

    return data
