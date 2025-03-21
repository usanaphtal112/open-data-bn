from rest_framework import serializers
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .validation import validate_email_field, validate_names, validate_password_fields
from .models import CustomUser, Review


class CustomUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
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
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "role",
            "profile_image",
            "date_joined",
        ]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            if request is not None:
                return request.build_absolute_uri(obj.profile_image.url)
            return f"{settings.MEDIA_URL}{obj.profile_image}"
        return None


class ReviewSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(write_only=True)
    object_id = serializers.IntegerField(write_only=True)
    content_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "comment",
            "content_type",
            "object_id",
            "content_object",
            "created_at",
        ]

    def validate_content_type(self, value):
        """Ensure the provided content_type corresponds to a valid model."""
        try:
            return ContentType.objects.get(model=value.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid content type. Make sure it is a valid model name."
            )

    def get_content_object(self, obj):
        """Return the name of the reviewed object."""
        return str(obj.content_object)
