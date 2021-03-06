import logging

from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import (
    UserSerializer,
    UserDetailSerializer
)

logger = logging.getLogger('api_server.user.views')


class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))


class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class UserInfoView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user
