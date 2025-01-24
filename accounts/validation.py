from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
import re as regex

User = get_user_model()


def validate_email_field(email):
    if not email:
        raise serializers.ValidationError({"email": "This field is required."})
    try:
        validate_email(email)
    except ValidationError:
        raise serializers.ValidationError({"email": "Enter a valid email address."})
    return email


def validate_names(first_name, last_name):
    if not first_name:
        raise serializers.ValidationError({"first_name": "This field is required."})
    if not first_name.isalpha():
        raise serializers.ValidationError(
            {"first_name": "Name should only contain letters."}
        )

    if not last_name:
        raise serializers.ValidationError({"last_name": "This field is required."})
    if not last_name.isalpha():
        raise serializers.ValidationError(
            {"last_name": "Name should only contain letters."}
        )

    return first_name, last_name


def validate_password_fields(password, confirm_password):
    if not password:
        raise serializers.ValidationError({"password": "This field is required."})
    if not confirm_password:
        raise serializers.ValidationError(
            {"confirm_password": "This field is required."}
        )

    if password != confirm_password:
        raise serializers.ValidationError({"password": "Passwords do not match."})

    if len(password) < 8:
        raise serializers.ValidationError(
            {"password": "Password must be at least 8 characters long."}
        )

    if not regex.search(r"^(?=.*[A-Z])(?=.*[a-z]).+$", password):
        raise serializers.ValidationError(
            {"password": "Password must contain at least one small and capital letter."}
        )

    if not regex.search(r".*\d+.*", password):
        raise serializers.ValidationError(
            {"password": "Password must contain at least one numerical value."}
        )

    if not regex.search(r"[!@#$%^&*()_+]", password):
        raise serializers.ValidationError(
            {"password": "Password must contain at least one special character."}
        )

    return password


def is_email_already_registered(email):
    User = get_user_model()
    return User.objects.filter(email=email).exists()
