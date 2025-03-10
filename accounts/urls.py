from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    CustomUserListAPIView,
    RefreshTokenAPIView,
    GetUserProfileAPIView,
)

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/refresh-token/", RefreshTokenAPIView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
    path("users/", CustomUserListAPIView.as_view(), name="users-lists"),
    path("users/profile/", GetUserProfileAPIView.as_view(), name="user-profile"),
]
