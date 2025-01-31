from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # profile_image = models.ImageField(
    #     upload_to="profile/", verbose_name=_("profile picture")
    # )
    profile_image_url = models.URLField(
        verbose_name=_("profile picture URL"), blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Blacklisted Token (Created: {self.blacklisted_at})"
