from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import LoginSerializer

# Register API Documentation
register_api_docs = swagger_auto_schema(
    operation_description="Register a new user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "first_name", "last_name", "password", "confirm_password"],
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="User's email"
            ),
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="User's first name"
            ),
            "middle_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="User's middle name (optional)"
            ),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="User's last name"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Password", format="password"
            ),
            "confirm_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Confirm password",
                format="password",
            ),
        },
    ),
    responses={
        201: openapi.Response(
            description="User registered successfully",
            examples={"application/json": {"message": "User registered successfully"}},
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={"application/json": {"detail": "Invalid input data"}},
        ),
        409: openapi.Response(
            description="Conflict",
            examples={
                "application/json": {"email": "This email is already registered."}
            },
        ),
    },
)

# Login API Documentation
login_api_docs = swagger_auto_schema(
    operation_description="Login user and get access token",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            description="Login successful",
            examples={"application/json": {"access_token": "string"}},
        ),
        401: openapi.Response(
            description="Invalid credentials",
            examples={"application/json": {"errors": ["Invalid credentials"]}},
        ),
    },
)

# Logout API Documentation
logout_api_docs = swagger_auto_schema(
    operation_description="Logout user by blacklisting the access token",
    responses={
        200: openapi.Response(
            description="Logout successful",
            examples={"application/json": {"message": "Successfully logged out"}},
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {"error": "Invalid token or no token provided"}
            },
        ),
    },
)

# Get Users API Documentation
get_users_api_docs = swagger_auto_schema(
    operation_description="Retrieve a list of all users",
    responses={
        200: openapi.Response(
            description="List of users retrieved successfully",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "email": "user@opendatahub.com",
                        "first_name": "Uwera",
                        "middle_name": "Angel",
                        "last_name": "Ineza",
                        "role": "USER",
                        "profile_image_url": "https://opendatahub.com/profile.jpg",
                        "date_joined": "2024-01-01T12:00:00Z",
                    }
                ]
            },
        )
    },
)
