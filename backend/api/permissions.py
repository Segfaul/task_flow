import re

from rest_framework import permissions

from .models import DashboardUser, Task


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
            return DashboardUser.objects.filter(dashboard_id=dashboard_id, user_id=user.id, role='creator').exists()
        except:
            return False
        

class IsDashboardUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            api_class = view.__class__.__name__
            class_headers = re.findall(r'[A-Z][a-z]*', api_class)

            if class_headers[0] == 'Dashboard':
                dashboard_id = view.kwargs.get('pk')

                return DashboardUser.objects.filter(dashboard_id=dashboard_id, user_id=request.user.id).exists()
            
            if class_headers[0] == 'Task':

                if request.method == 'GET':
                    task_id = view.kwargs.get('pk')

                    task = Task.objects.filter(id=task_id).get()

                    return DashboardUser.objects.filter(dashboard_id=task.dashboard, user_id=request.user.id).exists()
                
                if request.method == 'POST':
                    dashboard_id = request.data.get('dashboard')

                    dashboard_user = DashboardUser.objects.filter(dashboard_id=dashboard_id, user_id=request.user.id).get()
                    request.dashboard_user = dashboard_user

                    return dashboard_user is not None
                
                if request.method == 'PUT':
                    task_id = view.kwargs.get('pk')
                    task = Task.objects.filter(id=task_id).get()

                    dashboard_user = DashboardUser.objects.filter(dashboard_id=task.dashboard, user_id=request.user.id).get()

                    is_task_owner = (task.creator.id == dashboard_user.id) or (dashboard_user.role in ['creator', 'moderator'])

                    request.data['creator'] = task.creator.id
                    request.data['dashboard'] = task.dashboard.id

                    return is_task_owner

            return False

        except:
            return False
