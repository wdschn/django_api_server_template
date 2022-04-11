from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.permissions import AllowAny
from user.serializers import (
    UserSerializer,
    UserDetailSerializer
)


class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))


class UserInfoView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user
