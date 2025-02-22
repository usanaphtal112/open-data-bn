from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .location_data import PROVINCES, DISTRICTS, SECTORS, CELLS, VILLAGES
from .serializers import (
    ProvinceSerializer,
    DistrictSerializer,
    SectorSerializer,
    CellSerializer,
    VillageSerializer,
    SchoolLocationSerializer,
    SchoolDetailSerializer,
    SchoolListSerializer,
    SchoolCreateSerializer,
    SchoolImageSerializer,
    MultipleSchoolImageSerializer,
    SchoolFeesSerializer,
    SchoolContactSerializer,
    SchoolGovernmentDataSerializer,
    AlumniNetworkSerializer,
    AdmissionPolicySerializer,
)
from .models import School, SchoolChoices
from .validators import (
    validate_independent_location_codes,
    validate_hierarchical_location_codes,
    validate_school_filters,
)
from .swagger_docs import (
    get_province_docs,
    get_district_docs,
    get_sector_docs,
    get_cell_docs,
    get_village_docs,
    get_school_lists_docs,
    filter_school_by_location_docs,
    filter_school_by_location_hierarchical_docs,
    get_school_filters_docs,
    filter_school_docs,
    create_school_location_docs,
    get_school_details_docs,
)


class ProvinceAPIView(APIView):
    """
    API endpoint for retrieving provinces.

    This endpoint provides a list of all provinces with their codes and names.
    """

    @get_province_docs
    def get(self, request):
        provinces = [{"code": p[0], "name": p[1]} for p in PROVINCES]
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)


class DistrictAPIView(APIView):
    """
    API endpoint for retrieving districts.

    This endpoint provides districts for a specific province code.
    """

    @get_district_docs
    def get(self, request):
        province_code = request.query_params.get("province_code")
        districts = DISTRICTS.get(province_code, [])
        districts_data = [{"code": d[0], "name": d[1]} for d in districts]
        serializer = DistrictSerializer(districts_data, many=True)
        return Response(serializer.data)


class SectorAPIView(APIView):
    """
    API endpoint for retrieving sectors.

    This endpoint provides sectors for a specific district code.
    """

    @get_sector_docs
    def get(self, request):
        district_code = request.query_params.get("district_code")
        sectors = SECTORS.get(district_code, [])
        sectors_data = [{"code": s[0], "name": s[1]} for s in sectors]
        serializer = SectorSerializer(sectors_data, many=True)
        return Response(serializer.data)


class CellAPIView(APIView):
    """
    API endpoint for retrieving cells.

    This endpoint provides cells for a specific sector code.
    """

    @get_cell_docs
    def get(self, request):
        sector_code = request.query_params.get("sector_code")
        cells = CELLS.get(sector_code, [])
        cells_data = [{"code": c[0], "name": c[1]} for c in cells]
        serializer = CellSerializer(cells_data, many=True)
        return Response(serializer.data)


class VillageAPIView(APIView):
    """
    API endpoint for retrieving villages.

    This endpoint provides villages for a specific cell code.
    """

    @get_village_docs
    def get(self, request):
        cell_code = request.query_params.get("cell_code")
        villages = VILLAGES.get(cell_code, [])
        villages_data = [{"code": v[0], "name": v[1]} for v in villages]
        serializer = VillageSerializer(villages_data, many=True)
        return Response(serializer.data)


class SchoolCreateView(generics.CreateAPIView):
    """
    API endpoint for creating a new school.
    """

    serializer_class = SchoolCreateSerializer

    @swagger_auto_schema(
        operation_description="Create a new school",
        request_body=SchoolCreateSerializer,
        responses={
            201: SchoolCreateSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SchoolListAPIView(generics.ListAPIView):
    """
    API endpoint for retrieving a list of schools.

    This endpoint provides a list of all schools with their codes and names.
    """

    queryset = School.objects.all()
    serializer_class = SchoolListSerializer

    @get_school_lists_docs
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SchoolListByIndependentLocationAPIView(generics.ListAPIView):
    """
    API endpoint for retrieving a list of schools by location using unique codes.
    Location parameters can be provided independently since codes are unique.
    """

    serializer_class = SchoolDetailSerializer

    @filter_school_by_location_docs
    def get(self, request, *args, **kwargs):
        try:
            # Get and validate location parameters
            validate_independent_location_codes(
                province=request.query_params.get("province"),
                district=request.query_params.get("district"),
                sector=request.query_params.get("sector"),
                cell=request.query_params.get("cell"),
                village=request.query_params.get("village"),
            )
            return super().get(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = School.objects.all()

        # Apply filters for each location parameter if provided
        for param in ["province", "district", "sector", "cell", "village"]:
            value = self.request.query_params.get(param)
            if value:
                queryset = queryset.filter(**{f"schoollocation__{param}": value})

        return queryset.distinct()


class SchoolListByHierarchicalLocationAPIView(generics.ListAPIView):
    """
    API endpoint for retrieving a list of schools by location following hierarchical structure.
    Location parameters must be provided in hierarchical order (province -> district -> sector -> cell -> village).
    """

    serializer_class = SchoolDetailSerializer

    @filter_school_by_location_hierarchical_docs
    def get(self, request, *args, **kwargs):
        try:
            # Get and validate location parameters
            validate_hierarchical_location_codes(
                province=request.query_params.get("province"),
                district=request.query_params.get("district"),
                sector=request.query_params.get("sector"),
                cell=request.query_params.get("cell"),
                village=request.query_params.get("village"),
            )
            return super().get(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = School.objects.all()

        # Apply filters for each location parameter if provided
        for param in ["province", "district", "sector", "cell", "village"]:
            value = self.request.query_params.get(param)
            if value:
                queryset = queryset.filter(**{f"schoollocation__{param}": value})

        return queryset.distinct()


class SchoolFilterOptionsAPIView(APIView):
    """
    API endpoint that returns all possible filter options for schools.
    This helps frontend developers understand available choices for filtering schools.
    """

    @get_school_filters_docs
    def get(self, request):
        filter_options = {
            "ownership_types": [
                {"value": choice[0], "label": choice[1]}
                for choice in SchoolChoices.Ownership.choices
            ],
            "school_levels": [
                {"value": choice[0], "label": choice[1]}
                for choice in SchoolChoices.Level.choices
            ],
            "gender_types": [
                {"value": choice[0], "label": choice[1]}
                for choice in SchoolChoices.Gender.choices
            ],
            "school_types": [
                {"value": choice[0], "label": choice[1]}
                for choice in SchoolChoices.Type.choices
            ],
            "admission_types": [
                {"value": choice[0], "label": choice[1]}
                for choice in SchoolChoices.Admission.choices
            ],
            "discipline_types": [
                {"value": choice[0], "label": choice[1]}
                for choice in SchoolChoices.Discipline.choices
            ],
        }

        return Response(filter_options)


class SchoolListByFiltersAPIView(generics.ListAPIView):
    """
    API endpoint for retrieving schools filtered by various characteristics.
    All filter parameters are optional.
    """

    serializer_class = SchoolDetailSerializer

    @filter_school_docs
    def get(self, request, *args, **kwargs):
        try:
            # Get filter parameters
            filters = {
                "ownership": request.query_params.get("ownership"),
                "level": request.query_params.get("level"),
                "gender": request.query_params.get("gender"),
                "school_type": request.query_params.get("type"),
                "admission": request.query_params.get("admission"),
                "discipline": request.query_params.get("discipline"),
            }

            # Validate filters
            validate_school_filters(**filters)

            return super().get(request, *args, **kwargs)

        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = School.objects.all()

        # Apply ownership filter
        ownership = self.request.query_params.get("ownership")
        if ownership:
            queryset = queryset.filter(school_ownership=ownership)

        # Apply level filter
        level = self.request.query_params.get("level")
        if level:
            queryset = queryset.filter(school_level=level)

        # Apply gender filter
        gender = self.request.query_params.get("gender")
        if gender:
            queryset = queryset.filter(school_gender=gender)

        # Apply type filter
        school_type = self.request.query_params.get("type")
        if school_type:
            queryset = queryset.filter(school_type=school_type)

        # Apply admission policy filter
        admission = self.request.query_params.get("admission")
        if admission:
            queryset = queryset.filter(admissionpolicy__admission_policy=admission)

        # Apply discipline policy filter
        discipline = self.request.query_params.get("discipline")
        if discipline:
            queryset = queryset.filter(admissionpolicy__discipline_policy=discipline)

        return queryset.distinct()


class SchoolLocationCreateView(generics.CreateAPIView):
    """
    API endpoint for creating school locations.

    This endpoint allows creating a new school location with province, district,
    sector, cell, and village information.
    """

    serializer_class = SchoolLocationSerializer

    @create_school_location_docs
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SchoolDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving detailed information about a school.
    """

    queryset = School.objects.all()
    serializer_class = SchoolDetailSerializer

    @get_school_details_docs
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SchoolImageCreateView(generics.CreateAPIView):
    """
    API endpoint for uploading multiple images for a school.
    """

    serializer_class = MultipleSchoolImageSerializer

    @swagger_auto_schema(
        operation_description="Upload multiple school images",
        request_body=MultipleSchoolImageSerializer,
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING),
                    "uploaded_images": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                    ),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()  # This returns a list

        return Response(
            {
                "message": "Images uploaded successfully",
                "uploaded_images": SchoolImageSerializer(instances, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )


class SchoolFeesCreateView(generics.CreateAPIView):
    """
    API endpoint for creating school fees.
    """

    serializer_class = SchoolFeesSerializer

    @swagger_auto_schema(
        operation_description="Create school fees",
        request_body=SchoolFeesSerializer,
        responses={
            201: SchoolFeesSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SchoolContactCreateView(generics.CreateAPIView):
    """
    API endpoint for creating school contact details.
    """

    serializer_class = SchoolContactSerializer

    @swagger_auto_schema(
        operation_description="Create school contact details",
        request_body=SchoolContactSerializer,
        responses={
            201: SchoolContactSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AlumniNetworkCreateView(generics.CreateAPIView):
    """
    API endpoint for creating alumni network details.
    """

    serializer_class = AlumniNetworkSerializer

    @swagger_auto_schema(
        operation_description="Create alumni network details",
        request_body=AlumniNetworkSerializer,
        responses={
            201: AlumniNetworkSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SchoolGovernmentDataCreateView(generics.CreateAPIView):
    """
    API endpoint for creating school government data.
    """

    serializer_class = SchoolGovernmentDataSerializer

    @swagger_auto_schema(
        operation_description="Create school government data",
        request_body=SchoolGovernmentDataSerializer,
        responses={
            201: SchoolGovernmentDataSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AdmissionPolicyCreateView(generics.CreateAPIView):
    """
    API endpoint for creating admission policy details.
    """

    serializer_class = AdmissionPolicySerializer

    @swagger_auto_schema(
        operation_description="Create admission policy details",
        request_body=AdmissionPolicySerializer,
        responses={
            201: AdmissionPolicySerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
