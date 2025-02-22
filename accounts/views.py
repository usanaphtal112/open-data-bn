from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.utils.timezone import now
from datetime import timedelta
from .models import BlacklistedToken
from .serializers import CustomUserSerializer, LoginSerializer, GetCustomUserSerializer
from .validation import is_email_already_registered
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .swagger_docs import (
    register_api_docs,
    login_api_docs,
    logout_api_docs,
    get_users_api_docs,
)

User = get_user_model()


class RegisterAPIView(APIView):
    """
    API endpoint for user registration.

    **Required Fields**:
    - `email`
    - `first_name`
    - `last_name`
    - `password`
    - `confirm_password`

    **Optional Fields**:
    - `middle_name`
    """

    serializer_class = CustomUserSerializer

    @register_api_docs
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Database check only after all validations pass
        email = serializer.validated_data["email"]
        if is_email_already_registered(email):
            return Response(
                {"email": "This email is already registered."},
                status=status.HTTP_409_CONFLICT,
            )

        # Create user
        User = get_user_model()
        User.objects.create_user(
            email=email,
            first_name=serializer.validated_data["first_name"],
            middle_name=serializer.validated_data["middle_name"],
            last_name=serializer.validated_data["last_name"],
            password=serializer.validated_data["password"],
        )
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    """API endpoint for user login."""

    serializer_class = LoginSerializer

    @login_api_docs
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Validate credentials and get user
        try:
            user = authenticate(
                request=request,
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )

            if not user:
                return Response(
                    {"errors": ["Invalid credentials"]},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_401_UNAUTHORIZED)

        # Generate token
        token = RefreshToken.for_user(user)

        return Response(
            {
                "access_token": str(token.access_token),
                # "user": {
                #     "email": user.email,
                #     "first_name": user.first_name,
                #     "last_name": user.last_name,
                # },
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    """
    API endpoint for user logout.
    Blacklists the access token to prevent further use.
    """

    permission_classes = [IsAuthenticated]

    @logout_api_docs
    def post(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"error": "No valid token found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]

        with transaction.atomic():
            BlacklistedToken.objects.create(token=token, blacklisted_at=now())

            # Delete tokens older than 3 months
            expiry_date = now() - timedelta(days=90)
            BlacklistedToken.objects.filter(blacklisted_at__lt=expiry_date).delete()

        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )


class CustomUserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_users_api_docs
    def get(self, request):
        users = User.objects.all()
        serializer = GetCustomUserSerializer(users, many=True)
        return Response(serializer.data, status=200)
