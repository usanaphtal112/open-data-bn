from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
import secrets
import hashlib
from .serializers import CustomUserSerializer, LoginSerializer, GetCustomUserSerializer
from .validation import is_email_already_registered
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
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

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Generate fingerprint
        fingerprint = secrets.token_hex(32)
        fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()

        # Add fingerprint hash to the token payload
        refresh["fingerprint"] = fingerprint_hash
        access_token = refresh.access_token

        # Set the refresh token in a secure HttpOnly cookie
        response = Response(
            {
                "access_token": str(access_token),
                "token_type": "Bearer",
                # "user": {
                #    "email": user.email,
                #    "first_name": user.first_name,
                #    "last_name": user.last_name,
                # },
            },
            status=status.HTTP_200_OK,
        )
        # Set refresh token as HttpOnly cookie
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite="strict",
            max_age=60 * 60 * 24 * 7,
            path="/",  # Allow all routes to access this cookie
        )

        # Set fingerprint as HttpOnly cookie
        response.set_cookie(
            "fingerprint",
            fingerprint,
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite="strict",
            max_age=60 * 60 * 24 * 7,
            path="/",  # Allow all routes to access this cookie
        )

        return response


class RefreshTokenAPIView(APIView):
    """API endpoint for refreshing access tokens."""

    # @refresh_token_api_docs
    def post(self, request):
        # Get refresh token from cookie
        refresh_token = request.COOKIES.get("refresh_token")
        fingerprint = request.COOKIES.get("fingerprint")

        if not refresh_token or not fingerprint:
            return Response(
                {"error": "Refresh token or fingerprint missing"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            # Verify the refresh token
            refresh = RefreshToken(refresh_token)

            # Verify the fingerprint
            if "fingerprint" not in refresh:
                return Response(
                    {"error": "Invalid refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            stored_fingerprint_hash = refresh["fingerprint"]
            current_fingerprint_hash = hashlib.sha256(fingerprint.encode()).hexdigest()

            if stored_fingerprint_hash != current_fingerprint_hash:
                return Response(
                    {"error": "Invalid fingerprint"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Generate new tokens
            access_token = refresh.access_token

            # Return new access token
            return Response(
                {
                    "access_token": str(access_token),
                    "token_type": "bearer",
                },
                status=status.HTTP_200_OK,
            )

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutAPIView(APIView):
    """
    API endpoint for user logout.
    Blacklists the refresh token to prevent further use.
    """

    permission_classes = [IsAuthenticated]

    @logout_api_docs
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "No refresh token found"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get token and blacklist it
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Create response and clear cookies
            response = Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )

            # Clear the cookies
            response.delete_cookie("refresh_token", path="/")
            response.delete_cookie("fingerprint", path="/")

            return response

        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomUserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_users_api_docs
    def get(self, request):
        users = User.objects.all()
        serializer = GetCustomUserSerializer(users, many=True)
        return Response(serializer.data, status=200)


class GetUserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = GetCustomUserSerializer(user)
        return Response(serializer.data, status=200)
