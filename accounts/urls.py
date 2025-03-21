from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    CustomUserListAPIView,
    RefreshTokenAPIView,
    GetUserProfileAPIView,
    ListReviewsView,
    CreateReviewView,
    UpdateReviewView,
    DeleteReviewView,
)

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/refresh-token/", RefreshTokenAPIView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
    path("users/", CustomUserListAPIView.as_view(), name="users-lists"),
    path("users/profile/", GetUserProfileAPIView.as_view(), name="user-profile"),
    path("users/reviews/", ListReviewsView.as_view(), name="review-list"),
    path("users/reviews/create/", CreateReviewView.as_view(), name="review-create"),
    path(
        "users/reviews/update/<int:pk>/",
        UpdateReviewView.as_view(),
        name="review-update",
    ),
    path(
        "users/reviews/delete/<int:pk>/",
        DeleteReviewView.as_view(),
        name="review-delete",
    ),
]
