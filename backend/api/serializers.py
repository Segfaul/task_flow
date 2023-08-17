from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Task, Dashboard, DashboardUser, JoinRequest
from .validators import validate_user, validate_task


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
                         
    def validate(self, attrs):
        validate_user(attrs)
        return attrs

    class Meta:
        model = User
        fields = ('__all__')

    def check_user(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise serializers.ValidationError('user not found')
        return user
    
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        user_obj, created = User.objects.get_or_create(username=username)

        if created:
            user_obj.set_password(password)
            user_obj.save()
        else:
            raise serializers.ValidationError("Incorrect nickname or password")

        return user_obj
    

class TaskSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        instance = self.instance
        validate_task(instance, attrs)
        return attrs

    class Meta:
        model = Task
        fields = ('__all__')


class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        fields = ('__all__')


class DashboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardUser
        fields = ('__all__')


class DashboardSerializer(serializers.ModelSerializer):
    users = DashboardUserSerializer(many=True, required=False)
    tasks = TaskSerializer(many=True, required=False)
    join_requests = JoinRequestSerializer(many=True, required=False)

    class Meta:
        model = Dashboard
        fields = ('__all__')
