from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Review
import secrets
import hashlib
from .serializers import (
    CustomUserSerializer,
    LoginSerializer,
    GetCustomUserSerializer,
    ReviewSerializer,
)
from .validation import is_email_already_registered
from .swagger_docs import (
    register_api_docs,
    login_api_docs,
    logout_api_docs,
    get_users_api_docs,
    get_review_api_docs,
    create_review_api_docs,
    update_review_api_docs,
    delete_review_api_docs,
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
        serializer = GetCustomUserSerializer(user, context={"request": request})
        return Response(serializer.data, status=200)


class ListReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    @get_review_api_docs
    def get(self, request, *args, **kwargs):
        content_type = request.GET.get("content_type")
        object_id = request.GET.get("object_id")

        try:
            content_type_obj = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            return Response(
                {"error": "Invalid content_type"}, status=status.HTTP_400_BAD_REQUEST
            )

        reviews = Review.objects.filter(
            content_type=content_type_obj, object_id=object_id
        ).select_related("user")

        return Response(self.serializer_class(reviews, many=True).data)


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    @create_review_api_docs
    def post(self, request, *args, **kwargs):
        data = request.data
        content_type = data.get("content_type")
        object_id = data.get("object_id")

        try:
            content_type_obj = ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            return Response(
                {"error": "Invalid content_type"}, status=status.HTTP_400_BAD_REQUEST
            )

        review = Review.objects.create(
            user=request.user,
            rating=data["rating"],
            comment=data.get("comment", ""),
            content_type=content_type_obj,
            object_id=object_id,
        )

        # Update ratings immediately after saving
        Review.update_ratings(content_type_obj, object_id)

        return Response(
            {"message": "Review added successfully"}, status=status.HTTP_201_CREATED
        )


class UpdateReviewView(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    @update_review_api_docs
    def put(self, request, pk, *args, **kwargs):
        """
        Updates a review while ensuring the average rating is recalculated.
        """
        try:
            review = self.get_queryset().get(pk=pk)

            # Ensure the user updating the review is the one who created it
            if review.user != request.user:
                return Response(
                    {"error": "You can only update your own review"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Update the fields based on user input
            review.rating = request.data.get("rating", review.rating)
            review.comment = request.data.get("comment", review.comment)
            review.save()

            # Update the ratings immediately after modifying the review
            Review.update_ratings(review.content_type, review.object_id)

            return Response(
                {"message": "Review updated successfully"}, status=status.HTTP_200_OK
            )

        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteReviewView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    @delete_review_api_docs
    def delete(self, request, pk):
        try:
            review = self.get_queryset().get(pk=pk)
            content_type = review.content_type
            object_id = review.object_id
            review.delete()

            # Update ratings immediately after deleting
            Review.update_ratings(content_type, object_id)

            return Response(status=204)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=404)
