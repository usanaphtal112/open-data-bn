from django.urls import path
from .views import (
    ProvinceAPIView,
    DistrictAPIView,
    SectorAPIView,
    CellAPIView,
    VillageAPIView,
    SchoolLocationCreateView,
    DetailedSchoolAPIView,
)

urlpatterns = [
    path("provinces/", ProvinceAPIView.as_view(), name="provinces"),
    path("districts/", DistrictAPIView.as_view(), name="districts"),
    path("sectors/", SectorAPIView.as_view(), name="sectors"),
    path("cells/", CellAPIView.as_view(), name="cells"),
    path("villages/", VillageAPIView.as_view(), name="villages"),
    path(
        "school-locations/",
        SchoolLocationCreateView.as_view(),
        name="school-location-create",
    ),
    path("schools/<int:pk>/", DetailedSchoolAPIView.as_view(), name="school-detail"),
]
