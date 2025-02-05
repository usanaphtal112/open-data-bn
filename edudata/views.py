from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
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
    SchoolSerializer,
)
from .models import SchoolLocation, School


class ProvinceAPIView(APIView):
    """
    API endpoint for retrieving provinces.

    This endpoint provides a list of all provinces with their codes and names.
    """

    @swagger_auto_schema(
        operation_description="Get list of all provinces",
        responses={
            200: openapi.Response(
                description="List of provinces retrieved successfully",
                examples={
                    "application/json": [{"code": "RW.KG", "name": "KIGALI CITY"}]
                },
            )
        },
    )
    def get(self, request):
        provinces = [{"code": p[0], "name": p[1]} for p in PROVINCES]
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)


class DistrictAPIView(APIView):
    """
    API endpoint for retrieving districts.

    This endpoint provides districts for a specific province code.
    """

    @swagger_auto_schema(
        operation_description="Get districts for a specific province",
        manual_parameters=[
            openapi.Parameter(
                "province_code",
                openapi.IN_QUERY,
                description="Province code (e.g., 'RW.KG' for KIGALI CITY)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="List of districts retrieved successfully",
                examples={"application/json": [{"code": "0101", "name": "NYARUGENGE"}]},
            ),
            400: openapi.Response(
                description="Bad Request - Invalid or missing province_code",
                examples={"application/json": {"error": "province_code is required"}},
            ),
        },
    )
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

    @swagger_auto_schema(
        operation_description="Get sectors for a specific district",
        manual_parameters=[
            openapi.Parameter(
                "district_code",
                openapi.IN_QUERY,
                description="District code (e.g., 'RW.KG.NY' for NYARUGENGE)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="List of sectors retrieved successfully",
                examples={
                    "application/json": [{"code": "RW.KG.NY.GT", "name": "GITEGA"}]
                },
            ),
            400: openapi.Response(
                description="Bad Request - Invalid or missing district_code",
                examples={"application/json": {"error": "district_code is required"}},
            ),
        },
    )
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

    @swagger_auto_schema(
        operation_description="Get cells for a specific sector",
        manual_parameters=[
            openapi.Parameter(
                "sector_code",
                openapi.IN_QUERY,
                description="Sector code (e.g., 'RW.KG.NY.GT' for GITEGA)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="List of cells retrieved successfully",
                examples={
                    "application/json": [
                        {"code": "RW.KG.NY.GT.AK", "name": "AKABAHIZI"}
                    ]
                },
            ),
            400: openapi.Response(
                description="Bad Request - Invalid or missing sector_code",
                examples={"application/json": {"error": "sector_code is required"}},
            ),
        },
    )
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

    @swagger_auto_schema(
        operation_description="Get villages for a specific cell",
        manual_parameters=[
            openapi.Parameter(
                "cell_code",
                openapi.IN_QUERY,
                description="Cell code (e.g., 'RW.KG.NY.GT.AK' for AKABAHIZI)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="List of villages retrieved successfully",
                examples={
                    "application/json": [
                        {"code": "RW.KG.NY.GT.AK.GH", "name": "GIHANGA"}
                    ]
                },
            ),
            400: openapi.Response(
                description="Bad Request - Invalid or missing cell_code",
                examples={"application/json": {"error": "cell_code is required"}},
            ),
        },
    )
    def get(self, request):
        cell_code = request.query_params.get("cell_code")
        villages = VILLAGES.get(cell_code, [])
        villages_data = [{"code": v[0], "name": v[1]} for v in villages]
        serializer = VillageSerializer(villages_data, many=True)
        return Response(serializer.data)


class SchoolLocationCreateView(generics.CreateAPIView):
    """
    API endpoint for creating school locations.

    This endpoint allows creating a new school location with province, district,
    sector, cell, and village information.
    """

    queryset = SchoolLocation.objects.all()
    serializer_class = SchoolLocationSerializer

    @swagger_auto_schema(
        operation_description="Create a new school location",
        request_body=SchoolLocationSerializer,
        responses={
            201: openapi.Response(
                description="School location created successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "province_code": "RW.KG",
                        "district_code": "RW.KG.NY",
                        "sector_code": "RW.KG.NY.GT",
                        "cell_code": "RW.KG.NY.GT.AK",
                        "village_code": "RW.KG.NY.GT.AK.GH",
                    }
                },
            ),
            400: openapi.Response(
                description="Bad Request - Invalid data",
                examples={
                    "application/json": {
                        "province_code": ["This field is required."],
                        "district_code": ["This field is required."],
                        "sector_code": ["This field is required."],
                        "cell_code": ["This field is required."],
                        "village_code": ["This field is required."],
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DetailedSchoolAPIView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @swagger_auto_schema(
        operation_description="Get detailed information about a specific school",
        responses={200: SchoolSerializer, 404: "School not found"},
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Primary key ID of the school to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
