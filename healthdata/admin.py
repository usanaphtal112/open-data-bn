from django.contrib import admin
from .models import (
    HealthFacility,
    HealthFacilityLocation,
    Service,
    HealthFacilityServices,
    FacilityResources,
    HealthFacilityPopulation,
    FacilityFees,
    ContactInformation,
    GovernmentData,
    AdvancedFacilityData,
    FacilityImage,
)
from .forms import HealthFacilityLocationForm


class FacilityImageInline(admin.TabularInline):
    model = FacilityImage
    extra = 1
    fields = ("image", "caption", "image_type")


@admin.register(HealthFacility)
class HealthFacilityAdmin(admin.ModelAdmin):
    list_display = (
        "facility_code",
        "facility_name",
        "facility_type",
        "ownership",
        "created_at",
    )
    search_fields = ("facility_code", "facility_name")
    list_filter = ("facility_type", "ownership", "created_at")
    inlines = [FacilityImageInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("service_name",)
    search_fields = ("service_name",)


@admin.register(HealthFacilityServices)
class HealthFacilityServicesAdmin(admin.ModelAdmin):
    list_display = ("facility", "accreditation_status", "emergency_services")
    search_fields = ("facility__facility_name",)
    list_filter = ("accreditation_status", "emergency_services")


@admin.register(FacilityResources)
class FacilityResourcesAdmin(admin.ModelAdmin):
    list_display = ("facility", "beds", "special_needs_support")
    search_fields = ("facility__facility_name",)
    list_filter = ("special_needs_support",)


@admin.register(HealthFacilityPopulation)
class HealthFacilityPopulationAdmin(admin.ModelAdmin):
    list_display = ("facility", "year", "total_patients", "total_staff")
    search_fields = ("facility__facility_name",)
    list_filter = ("year",)


@admin.register(FacilityFees)
class FacilityFeesAdmin(admin.ModelAdmin):
    list_display = ("facility", "consultation_fee", "insurance_accepted")
    search_fields = ("facility__facility_name",)
    list_filter = ("insurance_accepted",)


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ("facility", "phone", "email", "website")
    search_fields = ("facility__facility_name", "phone", "email")


@admin.register(GovernmentData)
class GovernmentDataAdmin(admin.ModelAdmin):
    list_display = ("facility", "registration_date", "government_support")
    search_fields = ("facility__facility_name",)
    list_filter = ("government_support", "registration_date")


@admin.register(AdvancedFacilityData)
class AdvancedFacilityDataAdmin(admin.ModelAdmin):
    list_display = ("facility",)
    search_fields = ("facility__facility_name",)


@admin.register(FacilityImage)
class FacilityImageAdmin(admin.ModelAdmin):
    list_display = ("facility", "image_type", "uploaded_at")
    search_fields = ("facility__facility_name",)
    list_filter = ("image_type", "uploaded_at")


@admin.register(HealthFacilityLocation)
class SchoolLocationAdmin(admin.ModelAdmin):
    form = HealthFacilityLocationForm
    list_display = (
        "facility",
        "province",
        "district",
        "sector",
        "cell",
        "village",
        "latitude",
        "longitude",
    )
    list_filter = ("province", "district")
    search_fields = ("facility__facility_name",)

    class Media:
        js = ("admin/js/location_filter.js",)
