from rest_framework import serializers
from .validation import validate_email_field, validate_names, validate_password_fields
from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    confirm_password = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        # Validate email first
        email = validate_email_field(data.get("email"))

        # Then validate names
        first_name, middle_name, last_name = validate_names(
            data.get("first_name"), data.get("middle_name"), data.get("last_name")
        )

        # Finally validate password
        password = validate_password_fields(
            data.get("password"), data.get("confirm_password")
        )

        # Return validated data
        return {
            "email": email,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "password": password,
            "confirm_password": data.get("confirm_password"),
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        # Validate email
        email = validate_email_field(data.get("email"))

        # Validate password
        password = validate_password_fields(data.get("password"), data.get("password"))

        return {"email": email, "password": password}


class GetCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "role",
            "profile_image_url",
            "date_joined",
        ]
