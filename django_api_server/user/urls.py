from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from user.views import (
    UserView,
    UserInfoView,
    UserLoginView,
)

urlpatterns = [
    path('register', UserView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='user_login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('info', UserInfoView.as_view(), name='user_info'),
]
