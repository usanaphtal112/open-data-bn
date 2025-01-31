from django.contrib import admin
from .models import (
    School,
    SchoolImage,
    SchoolFees,
    SchoolLocation,
    SchoolContact,
    AlumniNetwork,
    SchoolGovernmentData,
    AdmissionPolicy,
)
from .forms import SchoolLocationForm


class SchoolImageInline(admin.TabularInline):
    model = SchoolImage
    extra = 1
    fields = ("image",)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = (
        "school_name",
        "school_type",
        "school_level",
        "average_rating",
        "review_count",
    )
    list_filter = ("school_type", "school_level", "school_ownership")
    search_fields = ("school_name",)
    inlines = [SchoolImageInline]


@admin.register(SchoolImage)
class SchoolImageAdmin(admin.ModelAdmin):
    list_display = ("school", "image", "created_at")
    list_filter = ("school",)
    search_fields = ("school__school_name",)


@admin.register(SchoolFees)
class SchoolFeesAdmin(admin.ModelAdmin):
    list_display = ("school", "currency", "amount")
    list_filter = ("currency",)
    search_fields = ("school__school_name",)


@admin.register(SchoolContact)
class SchoolContactAdmin(admin.ModelAdmin):
    list_display = ("school", "phone_number", "email", "website")
    search_fields = ("school__school_name", "phone_number", "email")


@admin.register(AlumniNetwork)
class AlumniNetworkAdmin(admin.ModelAdmin):
    list_display = ("school", "created_at")
    search_fields = ("school__school_name",)


@admin.register(SchoolGovernmentData)
class SchoolGovernmentDataAdmin(admin.ModelAdmin):
    list_display = ("school", "government_supported", "registration_date")
    list_filter = ("government_supported",)
    search_fields = ("school__school_name",)


@admin.register(AdmissionPolicy)
class AdmissionPolicyAdmin(admin.ModelAdmin):
    list_display = (
        "school",
        "admission_policy",
        "discipline_policy",
        "parental_engagement",
    )
    list_filter = ("admission_policy", "discipline_policy")
    search_fields = ("school__school_name",)


@admin.register(SchoolLocation)
class SchoolLocationAdmin(admin.ModelAdmin):
    form = SchoolLocationForm
    list_display = ("school", "province", "district", "sector", "cell", "village")
    list_filter = ("province", "district")
    search_fields = ("school__school_name",)

    class Media:
        js = ("admin/js/location_filter.js",)
