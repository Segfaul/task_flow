from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import *


schema_view = get_schema_view(
    openapi.Info(
        title="Task Flow API",
        default_version='v1',
        description="Task Flow - is a microservice for managing tasks "
                    "and ensuring efficient communication through the data bus. ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    patterns=[path('api/', include('api.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('user/', UserView.as_view(), name='user'),
    path('user/list/', UserListView.as_view(), name='user_list'),

    path('task/add/', TaskAddView.as_view(), name='task-add'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/', TaskGetView.as_view(), name='task-get'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    
    path('dashboard/add/', DashboardAddView.as_view(), name='dashboard-add'),
    path('dashboard/<int:pk>/', DashboardGetView.as_view(), name='dashboard-get'),
    path('dashboard/<int:pk>/delete/', DashboardDeleteView.as_view(), name='dashboard-delete')
]
