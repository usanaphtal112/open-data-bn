from rest_framework import serializers, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import (
    HealthFacility,
    HealthFacilityLocation,
    HealthFacilityServices,
    FacilityResources,
    ContactInformation,
    FacilityFees,
    HealthFacilityPopulation,
    GovernmentData,
    AdvancedFacilityData,
    FacilityImage,
)
from .Serializers import (
    HealthFacilitySerializer,
    HealthFacilityListSerializer,
    HealthFacilityCreateSerializer,
    HealthFacilityUpdateSerializer,
    LocationSerializer,
    ServicesSerializer,
    ResourcesSerializer,
    ContactSerializer,
    PopulationStatsSerializer,
    FacilityFeesSerializer,
    GovernmentDataSerializer,
    AdvancedDataSerializer,
    FacilityImageBulkSerializer,
    FacilityImageSerializer,
)


class HealthFacilityCreateView(APIView):
    """API view for creating health facilities"""

    @swagger_auto_schema(
        operation_description="Create a new health facility",
        request_body=HealthFacilityCreateSerializer,
        responses={
            201: HealthFacilityCreateSerializer,
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
        """Create a new health facility"""
        serializer = HealthFacilityCreateSerializer(
            data=request.data, context={"request": request}
        )
        try:
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                facility = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class HealthFacilityListView(generics.ListAPIView):
    """API view for listing health facilities"""

    queryset = HealthFacility.objects.prefetch_related(
        "location", "contact_info", "services", "images"
    )
    serializer_class = HealthFacilityListSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of health facilities with summarized details.",
        responses={
            200: openapi.Response(
                description="List of health facilities with limited details.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "facility_name": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Name of the health facility.",
                            ),
                            "facility_type": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Type of the health facility.",
                            ),
                            "level": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Level of the health facility.",
                            ),
                            "ownership": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Ownership type of the facility.",
                            ),
                            "average_rating": openapi.Schema(
                                type=openapi.TYPE_NUMBER,
                                format=openapi.FORMAT_FLOAT,
                                description="Average rating based on user reviews.",
                            ),
                            "verified": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description="Indicates if the facility is verified.",
                            ),
                            "address": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Physical address of the facility.",
                            ),
                            "service_name": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Main service offered by the facility.",
                            ),
                            "phone": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Primary contact phone number.",
                            ),
                            "whatsapp": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="WhatsApp contact number.",
                            ),
                            "review_count": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Number of users who have rated this facility.",
                            ),
                            "image_url": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_URI,
                                description="URL of the facility's main image.",
                            ),
                        },
                    ),
                ),
            )
        },
    )
    def get(self, request, *args, **kwargs):
        """List all health facilities with summarized details"""
        return super().get(request, *args, **kwargs)


class HealthFacilityDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get details of a specific health facility",
        responses={
            200: HealthFacilitySerializer,
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def get(self, request, facility_id):
        """Get a specific health facility by ID"""
        try:
            # Use select_related and prefetch_related to optimize queries
            facility = (
                HealthFacility.objects.select_related(
                    "location",
                    "services",
                    "resources",
                    "contact_info",
                    "fees",
                    "government_data",
                    "advanced_data",
                )
                .prefetch_related(
                    "population_stats", "images", "services__offered_services"
                )
                .get(id=facility_id)
            )

            serializer = HealthFacilitySerializer(facility)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": ["Health facility not found"]},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update a health facility",
        request_body=HealthFacilityUpdateSerializer,
        responses={
            200: HealthFacilityUpdateSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def put(self, request, facility_id):
        """Update a health facility"""
        try:
            facility = get_object_or_404(HealthFacility, id=facility_id)
            serializer = HealthFacilityUpdateSerializer(
                facility, data=request.data, partial=True, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    )
    def delete(self, request, facility_id):
        """Delete a health facility"""
        facility = get_object_or_404(HealthFacility, id=facility_id)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create location details for a health facility",
        request_body=LocationSerializer,
        responses={
            201: LocationSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Health facility not found",
                    )
                },
            ),
        },
    )
    def post(self, request, facility_id):
        """Create location details for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            serializer = LocationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class LocationDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get location details for a health facility",
        responses={
            200: LocationSerializer,
            404: "Health facility or location not found",
        },
    )
    def get(self, request, facility_id):
        """Get location details for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            location = HealthFacilityLocation.objects.get(facility=facility)
            serializer = LocationSerializer(location)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityLocation.DoesNotExist:
            return Response(
                {"error": "Location not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update location details for a health facility",
        request_body=LocationSerializer,
        responses={
            200: LocationSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Health facility or location not found",
                    )
                },
            ),
        },
    )
    def put(self, request, facility_id):
        """Update location details for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            location = HealthFacilityLocation.objects.get(facility=facility)
            serializer = LocationSerializer(location, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityLocation.DoesNotExist:
            return Response(
                {"error": "Location not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete location details for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Health facility or location not found",
                    )
                },
            ),
        },
    )
    def delete(self, request, facility_id):
        """Delete location details for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            location = HealthFacilityLocation.objects.get(facility=facility)
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityLocation.DoesNotExist:
            return Response(
                {"error": "Location not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ServicesCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create services information for a health facility",
        request_body=ServicesSerializer,
        responses={
            201: ServicesSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request, facility_id):
        """Create services information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            serializer = ServicesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class HealthFacilityServicesDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get services information for a health facility",
        responses={
            200: ServicesSerializer,
            404: "Health facility or services information not found",
        },
    )
    def get(self, request, facility_id):
        """Get services information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            services = HealthFacilityServices.objects.get(facility=facility)
            serializer = ServicesSerializer(services)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityServices.DoesNotExist:
            return Response(
                {"error": "Services information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update services information for a health facility",
        request_body=ServicesSerializer,
        responses={
            200: ServicesSerializer,
            400: "Bad Request",
            404: "Health facility or services information not found",
        },
    )
    def put(self, request, facility_id):
        """Update services information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            services = HealthFacilityServices.objects.get(facility=facility)
            serializer = ServicesSerializer(services, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityServices.DoesNotExist:
            return Response(
                {"error": "Services information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete services information for a health facility",
        responses={
            204: "No content",
            404: "Health facility or services information not found",
        },
    )
    def delete(self, request, facility_id):
        """Delete services information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            services = HealthFacilityServices.objects.get(facility=facility)
            services.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityServices.DoesNotExist:
            return Response(
                {"error": "Services information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class FacilityResourcesCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create resources information for a health facility",
        request_body=ResourcesSerializer,
        responses={
            201: ResourcesSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request, facility_id):
        """Create resources information for a specific health facility"""
        try:
            # First verify the facility exists
            facility = get_object_or_404(HealthFacility, id=facility_id)

            # Check if resources already exist for this facility
            if FacilityResources.objects.filter(facility=facility).exists():
                return Response(
                    {"error": "Resources already exist for this facility"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = ResourcesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class FacilityResourcesDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get resources details for a health facility",
        responses={
            200: ResourcesSerializer,
            404: "Health facility or resources not found",
        },
    )
    def get(self, request, facility_id):
        """Get resources details for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            resources = FacilityResources.objects.get(facility=facility)
            serializer = ResourcesSerializer(resources)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityResources.DoesNotExist:
            return Response(
                {"error": "Resources not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update resources information for a health facility",
        request_body=ResourcesSerializer,
        responses={
            200: ResourcesSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def put(self, request, facility_id):
        """Update resources information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            resources = FacilityResources.objects.get(facility=facility)
            serializer = ResourcesSerializer(resources, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityResources.DoesNotExist:
            return Response(
                {"error": "Resources not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete resources information for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def delete(self, request, facility_id):
        """Delete resources information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            resources = FacilityResources.objects.get(facility=facility)
            resources.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityResources.DoesNotExist:
            return Response(
                {"error": "Resources not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ContactInformationCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create contact information for a health facility",
        request_body=ContactSerializer,
        responses={
            201: ContactSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request, facility_id):
        """Create contact information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            serializer = ContactSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class ContactInformationDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get contact information for a health facility",
        responses={
            200: ContactSerializer,
            404: "Health facility or contact information not found",
        },
    )
    def get(self, request, facility_id):
        """Get contact information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            contact_info = ContactInformation.objects.get(facility=facility)
            serializer = ContactSerializer(contact_info)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ContactInformation.DoesNotExist:
            return Response(
                {"error": "Contact information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update contact information for a health facility",
        request_body=ContactSerializer,
        responses={
            200: ContactSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def put(self, request, facility_id):
        """Update contact information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            contact_info = ContactInformation.objects.get(facility=facility)
            serializer = ContactSerializer(
                contact_info, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ContactInformation.DoesNotExist:
            return Response(
                {"error": "Contact information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete contact information for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def delete(self, request, facility_id):
        """Delete contact information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            contact_info = ContactInformation.objects.get(facility=facility)
            contact_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ContactInformation.DoesNotExist:
            return Response(
                {"error": "Contact information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class HealthFacilityPopulationCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create population statistics for a health facility",
        request_body=PopulationStatsSerializer,
        responses={
            201: PopulationStatsSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request, facility_id):
        """Create population statistics for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            serializer = PopulationStatsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class HealthFacilityPopulationDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get population statistics for a health facility",
        responses={
            200: PopulationStatsSerializer,
            404: "Health facility or population statistics not found",
        },
    )
    def get(self, request, facility_id):
        """Get population statistics for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            population = HealthFacilityPopulation.objects.get(facility=facility)
            serializer = PopulationStatsSerializer(population)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityPopulation.DoesNotExist:
            return Response(
                {"error": "Population statistics not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update population statistics for a health facility",
        request_body=PopulationStatsSerializer,
        responses={
            200: PopulationStatsSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def put(self, request, facility_id, population_id):
        """Update population statistics for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            population = HealthFacilityPopulation.objects.get(
                id=population_id, facility=facility
            )
            serializer = PopulationStatsSerializer(
                population, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityPopulation.DoesNotExist:
            return Response(
                {"error": "Population statistics not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete population statistics for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def delete(self, request, facility_id, population_id):
        """Delete population statistics for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            population = HealthFacilityPopulation.objects.get(
                id=population_id, facility=facility
            )
            population.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except HealthFacilityPopulation.DoesNotExist:
            return Response(
                {"error": "Population statistics not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class FacilityFeesCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create fee information for a health facility",
        request_body=FacilityFeesSerializer,
        responses={
            201: FacilityFeesSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request, facility_id):
        """Create fee information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            serializer = FacilityFeesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class FacilityFeesDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get fee information for a health facility",
        responses={
            200: FacilityFeesSerializer,
            404: "Health facility or fee information not found",
        },
    )
    def get(self, request, facility_id):
        """Get fee information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            fees = FacilityFees.objects.get(facility=facility)
            serializer = FacilityFeesSerializer(fees)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityFees.DoesNotExist:
            return Response(
                {"error": "Fee information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update fee information for a health facility",
        request_body=FacilityFeesSerializer,
        responses={
            200: FacilityFeesSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def put(self, request, facility_id):
        """Update fee information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            fees = FacilityFees.objects.get(facility=facility)
            serializer = FacilityFeesSerializer(fees, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityFees.DoesNotExist:
            return Response(
                {"error": "Fee information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete fee information for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def delete(self, request, facility_id):
        """Delete fee information for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            fees = FacilityFees.objects.get(facility=facility)
            fees.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityFees.DoesNotExist:
            return Response(
                {"error": "Fee information not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class GovernmentDataCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create government data for a health facility",
        request_body=GovernmentDataSerializer,
        responses={
            201: GovernmentDataSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request, facility_id):
        """Create government data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            serializer = GovernmentDataSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class GovernmentDataDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get government data for a health facility",
        responses={
            200: GovernmentDataSerializer,
            404: "Health facility or government data not found",
        },
    )
    def get(self, request, facility_id):
        """Get government data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            government_data = GovernmentData.objects.get(facility=facility)
            serializer = GovernmentDataSerializer(government_data)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except GovernmentData.DoesNotExist:
            return Response(
                {"error": "Government data not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update government data for a health facility",
        request_body=GovernmentDataSerializer,
        responses={
            200: GovernmentDataSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def put(self, request, facility_id):
        """Update government data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            government_data = GovernmentData.objects.get(facility=facility)
            serializer = GovernmentDataSerializer(
                government_data, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except GovernmentData.DoesNotExist:
            return Response(
                {"error": "Government data not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete government data for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def delete(self, request, facility_id):
        """Delete government data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            government_data = GovernmentData.objects.get(facility=facility)
            government_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except GovernmentData.DoesNotExist:
            return Response(
                {"error": "Government data not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class AdvancedFacilityDataCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Create advanced data for a health facility",
        request_body=AdvancedDataSerializer,
        responses={
            201: AdvancedDataSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request, facility_id):
        """Create advanced data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            serializer = AdvancedDataSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(facility=facility)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class AdvancedFacilityDataDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get advanced data for a health facility",
        responses={
            200: AdvancedDataSerializer,
            404: "Health facility or advanced data not found",
        },
    )
    def get(self, request, facility_id):
        """Get advanced data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            advanced_data = AdvancedFacilityData.objects.get(facility=facility)
            serializer = AdvancedDataSerializer(advanced_data)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except AdvancedFacilityData.DoesNotExist:
            return Response(
                {"error": "Advanced data not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update advanced data for a health facility",
        request_body=AdvancedDataSerializer,
        responses={
            200: AdvancedDataSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def put(self, request, facility_id):
        """Update advanced data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            advanced_data = AdvancedFacilityData.objects.get(facility=facility)
            serializer = AdvancedDataSerializer(
                advanced_data, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except AdvancedFacilityData.DoesNotExist:
            return Response(
                {"error": "Advanced data not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete advanced data for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def delete(self, request, facility_id):
        """Delete advanced data for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            advanced_data = AdvancedFacilityData.objects.get(facility=facility)
            advanced_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except AdvancedFacilityData.DoesNotExist:
            return Response(
                {"error": "Advanced data not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )


class FacilityImageBulkCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Bulk upload images for a health facility",
        request_body=FacilityImageBulkSerializer(many=True),
        responses={
            201: FacilityImageBulkSerializer(many=True),
            400: "Bad Request",
            404: "Health Facility Not Found",
        },
    )
    def post(self, request, facility_id):
        """Bulk upload images for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)

            # Create a list of data for each image
            data = []
            images = request.FILES.getlist("image")

            for image in images:
                image_data = {
                    "image": image,
                    "caption": request.data.get("caption"),
                    "image_type": request.data.get("image_type"),
                }
                data.append(image_data)
            serializer = FacilityImageBulkSerializer(
                data=data, many=True, context={"facility": facility}
            )

            if serializer.is_valid(raise_exception=True):
                saved_images = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FacilityImageDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Get an image for a health facility",
        responses={
            200: FacilityImageSerializer,
            404: "Health facility or image not found",
        },
    )
    def get(self, request, facility_id, image_id):
        """Get an image for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            image = FacilityImage.objects.get(id=image_id, facility=facility)
            serializer = FacilityImageSerializer(image)
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityImage.DoesNotExist:
            return Response(
                {"error": "Image not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_description="Update an image for a health facility",
        request_body=FacilityImageSerializer,
        responses={
            200: FacilityImageSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "field_name": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def put(self, request, facility_id, image_id):
        """Update an image for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            image = FacilityImage.objects.get(id=image_id, facility=facility)
            serializer = FacilityImageSerializer(image, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityImage.DoesNotExist:
            return Response(
                {"error": "Image not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an image for a health facility",
        responses={
            204: "No content",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        },
    )
    def delete(self, request, facility_id, image_id):
        """Delete an image for a specific health facility"""
        try:
            facility = HealthFacility.objects.get(id=facility_id)
            image = FacilityImage.objects.get(id=image_id, facility=facility)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HealthFacility.DoesNotExist:
            return Response(
                {"error": "Health facility not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except FacilityImage.DoesNotExist:
            return Response(
                {"error": "Image not found for this facility"},
                status=status.HTTP_404_NOT_FOUND,
            )
