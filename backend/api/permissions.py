from rest_framework import permissions
from rest_framework.exceptions import NotFound

from .models import Dashboard, DashboardUser, Task


class IsAdminUser(permissions.BasePermission):
    """
    Check user on admin rights
    """
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAnonymousUser(permissions.BasePermission):
    """
    Check if user is not logged in
    """
    def has_permission(self, request, view):
        return (not request.user.is_authenticated)


class BaseDashboardPermission(permissions.BasePermission):
    """
    Base class for dashboard permissions
    """
    def has_permission(self, request, view, role=None):
        try:
            dashboard_id = view.kwargs.get('pk')

            dashboard = Dashboard.objects.get(pk=dashboard_id)
            request.dashboard = dashboard

            filter_params = {'dashboard_id': dashboard_id, 'user_id': request.user.id}
            if role:
                filter_params['role'] = role

            return DashboardUser.objects.filter(**filter_params).exists()

        except Exception as error:
            if error.__class__ == Dashboard.DoesNotExist:
                raise NotFound("Dashboard not found")

            return False


class IsDashboardCreator(BaseDashboardPermission):
    """
    Check dashboard_user on creator dashboard rights
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view, role='creator')
     

class IsDashboardUser(BaseDashboardPermission):
    """
    Check dashboard_user on user dashboard rights
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view)


class IsTaskCreator(permissions.BasePermission):
    """
    Check dashboard_user on task owning rights
    """
    def has_permission(self, request, view):   
        try:
            
            if request.method == 'POST':
                dashboard_id = request.data.get('dashboard')

                dashboard_user = DashboardUser.objects.filter(dashboard_id=dashboard_id, user_id=request.user.id).get()
                request.data['creator'] = dashboard_user.id

                return not (dashboard_user.role == 'user' and all(item in request.data for item in ['answer', 'resolver']))
            
            if request.method in ['GET', 'PUT', 'DELETE']:
                task_id = view.kwargs.get('pk')
                task = Task.objects.filter(id=task_id).get()
                request.task = task

                dashboard_user = DashboardUser.objects.filter(dashboard_id=task.dashboard, user_id=request.user.id).get()
            
                if request.method == 'GET':
                    return dashboard_user is not None
                
                if request.method == 'PUT':
                    request.data['creator'] = task.creator.id
                    request.data['dashboard'] = task.dashboard.id

                is_task_related = (task.creator.id == dashboard_user.id and all(item not in request.data for item in ['answer', 'resolver'])) \
                                or (task.resolver.id == dashboard_id.id and 'answer' in request.data and len(request.data) == 1) \
                                or (dashboard_user.role in ['creator', 'moderator'])

                return is_task_related

            return False

        except Exception as error:
            print(error)
            if error.__class__ == Task.DoesNotExist:
                raise NotFound("Task not found")

            return False
