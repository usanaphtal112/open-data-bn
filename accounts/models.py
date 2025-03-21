from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import re as regex


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends the default Django user model.
    """

    def profile_image_path(instance, filename):
        # Sanitize school name for file path
        safe_profile_name = regex.sub(r"[^\w\-_]", "", instance.first_name).lower()
        return f"profile_images/{safe_profile_name}_photos/{filename}"

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
        BUSINESS_OWNER = "BUSINESS_OWNER", "Business Owner"

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.USER,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(
        upload_to=profile_image_path,
        verbose_name=_("profile picture"),
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} - {self.content_object} ({self.rating})"

    @staticmethod
    def update_ratings(content_type, object_id):
        """
        Efficiently updates the average_rating and review_count for the reviewed object.
        """

        review_aggregate = Review.objects.filter(
            content_type=content_type, object_id=object_id
        ).aggregate(avg_rating=models.Avg("rating"), count=models.Count("id"))

        avg_rating = review_aggregate["avg_rating"] or 0
        count = review_aggregate["count"]

        # Atomic Update using F expressions
        content_type.model_class().objects.filter(id=object_id).update(
            average_rating=models.F("average_rating") * 0 + avg_rating,
            review_count=models.F("review_count") * 0 + count,
        )
