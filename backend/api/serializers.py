from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Task
from .validators import validate_user


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
        user_obj = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user_obj.save()

        return user_obj
    

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('__all__')
