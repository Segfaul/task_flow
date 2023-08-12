from rest_framework import permissions

from .models import DashboardUser


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAnonymousUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (not request.user.is_authenticated)
    

class IsDashboardCreator(permissions.BasePermission):
    def has_permission(self, request, view):
        dashboard_id = view.kwargs.get('pk')
        user = request.user

        try:
            return DashboardUser.objects.get(dashboard_id=dashboard_id, user_id=user.id, role='creator')

        except:
            return False
        

class IsDashboardUser(permissions.BasePermission):
    def has_permission(self, request, view):
        dashboard_id = view.kwargs.get('pk')
        user = request.user

        try:
            return DashboardUser.objects.get(dashboard_id=dashboard_id, user_id=user.id, role='user')

        except:
            return False
