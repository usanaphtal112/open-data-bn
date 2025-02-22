from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, CustomUserListAPIView

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
    path("users/", CustomUserListAPIView.as_view(), name="users-lists"),
]
