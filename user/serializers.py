from rest_framework import serializers

from user.models import (
    User
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']
