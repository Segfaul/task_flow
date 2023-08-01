from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('task/', TaskGetView.as_view(), name='task_get'),
    path('task/create/', TaskAddView.as_view(), name='task_create'),
]
