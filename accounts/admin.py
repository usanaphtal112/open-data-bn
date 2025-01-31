from django.contrib import admin
from .models import CustomUser, BlacklistedToken
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("email", "first_name", "middle_name", "last_name", "role")
    search_fields = ("email", "first_name", "middle_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "middle_name", "last_name")}),
        ("Permissions", {"fields": ("role",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "role",
                ),
            },
        ),
    )


@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "blacklisted_at")
    search_fields = ("token",)
    readonly_fields = ("blacklisted_at",)
    ordering = ("-blacklisted_at",)


admin.site.register(CustomUser, CustomUserAdmin)
