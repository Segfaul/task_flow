from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (not request.user.is_authenticated)
