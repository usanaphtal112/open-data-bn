from rest_framework import serializers, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
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
from .swagger_docs import (
    get_facility_lists,
    get_facility_details,
    create_facility_services_docs,
    get_facility_services_details_docs,
    get_facility_resources_details_docs,
    get_facility_advanceddata_details_docs,
    get_facility_contactinfo_details_docs,
    get_facility_fees_details_docs,
    get_facility_governmentdata_details_docs,
    get_facility_images_details_docs,
    get_facility_location_details_docs,
    get_facility_population_details_docs,
    create_facility_governmentdata_docs,
    create_facility_advanceddata_docs,
    create_facility_contactinfo_docs,
    create_facility_fees_docs,
    create_facility_population_docs,
    create_facility_resources_docs,
    create_facility_location_docs,
    create_health_facility_docs,
    create_facility_images_docs,
    update_facility_advanceddata_docs,
    update_facility_contactinfo_docs,
    update_facility_fees_docs,
    update_facility_governmentdata_docs,
    update_facility_images_docs,
    update_facility_location_docs,
    update_facility_population_docs,
    update_facility_resources_docs,
    update_facility_services_docs,
    update_health_facility_docs,
    delete_health_facility_docs,
    delete_facility_advanceddata_docs,
    delete_facility_contactinfo_docs,
    delete_facility_location_docs,
    delete_facility_population_docs,
    delete_facility_advanceddata_docs,
    delete_facility_services_docs,
    delete_facility_resources_docs,
    delete_facility_fees_docs,
    delete_facility_governmentdata_docs,
)


class HealthFacilityCreateView(APIView):
    """API view for creating health facilities"""

    @create_health_facility_docs
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

    @get_facility_lists
    def get(self, request, *args, **kwargs):
        """List all health facilities with summarized details"""
        return super().get(request, *args, **kwargs)


class HealthFacilityDetailView(APIView):
    @get_facility_details
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

    @update_health_facility_docs
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

    @delete_health_facility_docs
    def delete(self, request, facility_id):
        """Delete a health facility"""
        facility = get_object_or_404(HealthFacility, id=facility_id)
        facility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocationCreateView(APIView):
    @create_facility_location_docs
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
    @get_facility_location_details_docs
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

    @update_facility_location_docs
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

    @delete_facility_location_docs
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
    @create_facility_services_docs
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
    @get_facility_services_details_docs
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

    @update_facility_services_docs
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

    @delete_facility_services_docs
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
    @create_facility_resources_docs
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
    @get_facility_resources_details_docs
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

    @update_facility_resources_docs
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

    @delete_facility_resources_docs
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
    @create_facility_contactinfo_docs
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
    @get_facility_contactinfo_details_docs
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

    @update_facility_contactinfo_docs
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

    @delete_facility_contactinfo_docs
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
    @create_facility_population_docs
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
    @get_facility_population_details_docs
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

    @update_facility_population_docs
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

    @delete_facility_population_docs
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
    @create_facility_fees_docs
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
    @get_facility_fees_details_docs
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

    @update_facility_fees_docs
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

    @delete_facility_fees_docs
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
    @create_facility_governmentdata_docs
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
    @get_facility_governmentdata_details_docs
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

    @update_facility_governmentdata_docs
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

    @delete_facility_governmentdata_docs
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
    @create_facility_advanceddata_docs
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
    @get_facility_advanceddata_details_docs
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

    @update_facility_advanceddata_docs
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

    @delete_facility_advanceddata_docs
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

    @create_facility_images_docs
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
    @get_facility_images_details_docs
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

    @update_facility_images_docs
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

    @delete_facility_governmentdata_docs
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
