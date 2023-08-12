from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer, TaskSerializer, DashboardSerializer, JoinRequestSerializer, DashboardUserSerializer
from .permissions import IsAdminUser, IsAnonymousUser, IsDashboardCreator, IsDashboardUser
from .models import User, Task, Dashboard, JoinRequest


class LoginView(APIView):
    """
    Sign in to your account if created
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAnonymousUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING),
            openapi.Parameter('Password', openapi.IN_QUERY, description="password", type=openapi.TYPE_STRING)
        ],
        responses={200: UserSerializer()}
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(request.data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Sign out of your account if created
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Create a new account
    """

    permission_classes = [IsAnonymousUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING),
            openapi.Parameter('Password', openapi.IN_QUERY, description="password", type=openapi.TYPE_STRING)
        ],
        responses={201: UserSerializer()}
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                login(request, user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    """
    Get your account info (only if authenticated)
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer()}
    )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UserListView(APIView):
    """
    Get list of all accounts (only if admin)
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        responses={200: UserSerializer()}
    )

    def get(self):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TaskAddView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['creator'] = request.user.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskUpdateView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        request.data['description'] = task.description
        request.data['creator'] = task.creator_id
        request.data['dashboard'] = task.dashboard_id
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskGetView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)

class TaskDeleteView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, creator=request.user)
        except Task.DoesNotExist:
            return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DashboardAddView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        dashboard_serializer = DashboardSerializer(data=request.data)

        if dashboard_serializer.is_valid():
            dashboard_serializer.save()

            user = request.user
            creator_data = {
                'user': user.id,
                'dashboard': dashboard_serializer.instance.id,
                'role': 'creator',
            }

            creator_serializer = DashboardUserSerializer(data=creator_data)
            if creator_serializer.is_valid():
                creator_serializer.save()
            else:
                dashboard_serializer.instance.delete()
                return Response(creator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(dashboard_serializer.data, status=status.HTTP_201_CREATED)
        return Response(dashboard_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardGetView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsDashboardUser]

    def get(self, request, pk):
        try:
            dashboard = Dashboard.objects.get(pk=pk)
        except Dashboard.DoesNotExist:
            return Response({'detail': 'Dashboard not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DashboardSerializer(dashboard)
        return Response(serializer.data)

class DashboardDeleteView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsDashboardCreator]

    def delete(self, request, pk):
        dashboard = Dashboard.objects.get(pk=pk)
        dashboard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class JoinRequestActionView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, join_request_id):
        user = request.user
        action = request.data.get('action')

        try:
            join_request = JoinRequest.objects.get(id=join_request_id, dashboard__creator=user)
            if action is not None:
                if action:
                    join_request.is_accepted = True
                    join_request.save()
                    dashboard = join_request.dashboard
                    dashboard.members.add(join_request.user)
                    return Response({'detail': 'Request accepted successfully.'}, status=status.HTTP_200_OK)
                else:
                    join_request.is_accepted = False
                    join_request.save()
                    return Response({'detail': 'Request rejected successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid action parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        except JoinRequest.DoesNotExist:
            return Response({'detail': 'Join request not found.'}, status=status.HTTP_404_NOT_FOUND)


class JoinRequestCreateView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class JoinRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        join_requests = JoinRequest.objects.filter(dashboard__creator=user)
        serializer = JoinRequestSerializer(join_requests, many=True)
        return Response(serializer.data)


class TaskGetListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
