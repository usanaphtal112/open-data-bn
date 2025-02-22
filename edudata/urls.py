from django.urls import path
from .views import (
    ProvinceAPIView,
    DistrictAPIView,
    SectorAPIView,
    CellAPIView,
    VillageAPIView,
    SchoolLocationCreateView,
    SchoolDetailView,
    SchoolListAPIView,
    SchoolListByHierarchicalLocationAPIView,
    SchoolListByIndependentLocationAPIView,
    SchoolFilterOptionsAPIView,
    SchoolListByFiltersAPIView,
    SchoolCreateView,
    SchoolImageCreateView,
    SchoolContactCreateView,
    SchoolFeesCreateView,
    AlumniNetworkCreateView,
    SchoolGovernmentDataCreateView,
    AdmissionPolicyCreateView,
)

urlpatterns = [
    path("provinces/", ProvinceAPIView.as_view(), name="provinces"),
    path("districts/", DistrictAPIView.as_view(), name="districts"),
    path("sectors/", SectorAPIView.as_view(), name="sectors"),
    path("cells/", CellAPIView.as_view(), name="cells"),
    path("villages/", VillageAPIView.as_view(), name="villages"),
    path("schools/", SchoolListAPIView.as_view(), name="school-list"),
    path("schools/<int:pk>/", SchoolDetailView.as_view(), name="school-detail"),
    path(
        "schools/by-location/independent/",
        SchoolListByIndependentLocationAPIView.as_view(),
        name="schools-by-location-independent",
    ),
    path(
        "schools/by-location/hierarchical/",
        SchoolListByHierarchicalLocationAPIView.as_view(),
        name="schools-by-location-hierarchical",
    ),
    path(
        "schools/filter-options/",
        SchoolFilterOptionsAPIView.as_view(),
        name="school-filter-options",
    ),
    path(
        "schools/filters/",
        SchoolListByFiltersAPIView.as_view(),
        name="schools-by-filters",
    ),
    path("schools/create/", SchoolCreateView.as_view(), name="school-create"),
    path(
        "school-locations/create/",
        SchoolLocationCreateView.as_view(),
        name="school-location-create",
    ),
    path(
        "schools/images-upload/",
        SchoolImageCreateView.as_view(),
        name="school-image-create",
    ),
    path(
        "schools/create-contact/",
        SchoolContactCreateView.as_view(),
        name="school-contact-create",
    ),
    path(
        "schools/create-fees/",
        SchoolFeesCreateView.as_view(),
        name="school-fees-create",
    ),
    path(
        "schools/create-alumni/",
        AlumniNetworkCreateView.as_view(),
        name="school-alumni-network-create",
    ),
    path(
        "schools/create-government-data/",
        SchoolGovernmentDataCreateView.as_view(),
        name="school-government-data-create",
    ),
    path(
        "schools/create-school-admission-policy/",
        AdmissionPolicyCreateView.as_view(),
        name="school-admission-policy-create",
    ),
]
