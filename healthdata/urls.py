from django.urls import path
from .views import (
    HealthFacilityListView,
    HealthFacilityDetailView,
    HealthFacilityCreateView,
    LocationCreateView,
    LocationDetailView,
    ServicesCreateView,
    HealthFacilityServicesDetailView,
    FacilityResourcesCreateView,
    FacilityResourcesDetailView,
    ContactInformationCreateView,
    ContactInformationDetailView,
    HealthFacilityPopulationCreateView,
    HealthFacilityPopulationDetailView,
    FacilityFeesCreateView,
    FacilityFeesDetailView,
    GovernmentDataCreateView,
    GovernmentDataDetailView,
    AdvancedFacilityDataCreateView,
    AdvancedFacilityDataDetailView,
    FacilityImageBulkCreateView,
    FacilityImageDetailView,
)

urlpatterns = [
    path("facilities/", HealthFacilityCreateView.as_view(), name="facility-create"),
    path("facilities/list/", HealthFacilityListView.as_view(), name="facility-list"),
    path(
        "facilities/<int:facility_id>/",
        HealthFacilityDetailView.as_view(),
        name="facility-detail",
    ),
    path(
        "facilities/<int:facility_id>/create-location/",
        LocationCreateView.as_view(),
        name="location-create",
    ),
    path(
        "facilities/<int:facility_id>/location/",
        LocationDetailView.as_view(),
        name="location-detail",
    ),
    path(
        "facilities/<int:facility_id>/create-services/",
        ServicesCreateView.as_view(),
        name="services-create",
    ),
    path(
        "facilities/<int:facility_id>/services/",
        HealthFacilityServicesDetailView.as_view(),
        name="services-detail",
    ),
    # Facility Resources URLs
    path(
        "facilities/<int:facility_id>/create-resources/",
        FacilityResourcesCreateView.as_view(),
        name="resources-create",
    ),
    path(
        "facilities/<int:facility_id>/resources/",
        FacilityResourcesDetailView.as_view(),
        name="resources-detail",
    ),
    # Contact Information URLs
    path(
        "facilities/<int:facility_id>/create-contact/",
        ContactInformationCreateView.as_view(),
        name="contact-create",
    ),
    path(
        "facilities/<int:facility_id>/contact/",
        ContactInformationDetailView.as_view(),
        name="contact-detail",
    ),
    # Population Stats URLs
    path(
        "facilities/<int:facility_id>/create-population/",
        HealthFacilityPopulationCreateView.as_view(),
        name="population-create",
    ),
    path(
        "facilities/<int:facility_id>/population/",
        HealthFacilityPopulationDetailView.as_view(),
        name="population-detail",
    ),
    # Facility Fees URLs
    path(
        "facilities/<int:facility_id>/create-fees/",
        FacilityFeesCreateView.as_view(),
        name="fees-create",
    ),
    path(
        "facilities/<int:facility_id>/fees/",
        FacilityFeesDetailView.as_view(),
        name="fees-detail",
    ),
    # Government Data URLs
    path(
        "facilities/<int:facility_id>/create-governmentdata/",
        GovernmentDataCreateView.as_view(),
        name="government-create",
    ),
    path(
        "facilities/<int:facility_id>/governmentdata/",
        GovernmentDataDetailView.as_view(),
        name="government-detail",
    ),
    # Advanced Facility Data URLs
    path(
        "facilities/<int:facility_id>/create-advanced/",
        AdvancedFacilityDataCreateView.as_view(),
        name="advanced-create",
    ),
    path(
        "facilities/<int:facility_id>/advanced/",
        AdvancedFacilityDataDetailView.as_view(),
        name="advanced-detail",
    ),
    # Facility Image URLs
    path(
        "facilities/<int:facility_id>/create-images/",
        FacilityImageBulkCreateView.as_view(),
        name="images-create",
    ),
    path(
        "facilities/<int:facility_id>/images/<int:image_id>/",
        FacilityImageDetailView.as_view(),
        name="images-detail",
    ),
]
