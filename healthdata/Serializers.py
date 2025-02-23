from rest_framework import serializers
from .models import (
    HealthFacility,
    HealthFacilityLocation,
    HealthFacilityServices,
    FacilityResources,
    ContactInformation,
    Service,
    FacilityImage,
    HealthFacilityPopulation,
    FacilityFees,
    GovernmentData,
    AdvancedFacilityData,
)
from edudata.location_data import PROVINCES, DISTRICTS, SECTORS, CELLS, VILLAGES
from .validators import (
    validate_special_programs,
    validate_performance_metrics,
    validate_laboratories,
)


class HealthFacilityListSerializer(serializers.ModelSerializer):
    """Serializer for listing health facilities with limited details"""

    address = serializers.CharField(source="location.address", read_only=True)
    service_name = serializers.SerializerMethodField()
    phone = serializers.CharField(source="contact_info.phone", read_only=True)
    whatsapp = serializers.CharField(source="contact_info.whatsapp", read_only=True)
    number_of_ratings = serializers.IntegerField(source="review_count", read_only=True)
    cover = serializers.SerializerMethodField()

    class Meta:
        model = HealthFacility
        fields = [
            "id",
            "facility_name",
            "facility_type",
            "level",
            "ownership",
            "average_rating",
            "verified",
            "address",
            "service_name",
            "phone",
            "whatsapp",
            "number_of_ratings",
            "cover",
        ]

    def get_service_name(self, obj):
        """
        Retrieves the first available service name for the facility.
        If the facility has no services, returns None.
        """
        if hasattr(obj, "services") and obj.services is not None:
            services = obj.services.offered_services.all()
            return services[0].service_name if services.exists() else None
        return None

    def get_cover(self, obj):
        """Retrieve the first image of the facility"""
        image = obj.images.first()
        return image.image.url if image else None


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthFacilityLocation
        exclude = ("id", "facility")

    def validate(self, data):
        # Validate coordinates if provided
        if data.get("latitude") and data.get("longitude"):
            latitude = float(data["latitude"])
            longitude = float(data["longitude"])

            if not (-90 <= latitude <= 90):
                raise serializers.ValidationError(
                    {"latitude": ["Latitude must be between -90 and 90."]}
                )
            if not (-180 <= longitude <= 180):
                raise serializers.ValidationError(
                    {"longitude": ["Longitude must be between -180 and 180."]}
                )

        # Check if required fields are present first
        required_fields = ["province", "district", "sector", "cell", "village"]
        errors = {}

        # Check for missing required fields
        for field in required_fields:
            if field not in data:
                errors[field] = ["This field is required."]

        if errors:
            raise serializers.ValidationError(errors)

        # If all required fields are present, validate the hierarchy
        if "province" in data:
            province = data["province"]
            if "district" in data:
                district = data["district"]
                valid_districts = [d[0] for d in DISTRICTS.get(province, [])]
                if district not in valid_districts:
                    errors["district"] = [
                        "Invalid district code for the selected province"
                    ]

                if "sector" in data:
                    sector = data["sector"]
                    valid_sectors = [s[0] for s in SECTORS.get(district, [])]
                    if sector not in valid_sectors:
                        errors["sector"] = [
                            "Invalid sector code for the selected district"
                        ]

                    if "cell" in data:
                        cell = data["cell"]
                        valid_cells = [c[0] for c in CELLS.get(sector, [])]
                        if cell not in valid_cells:
                            errors["cell"] = [
                                "Invalid cell code for the selected sector"
                            ]

                        if "village" in data:
                            village = data["village"]
                            valid_villages = [v[0] for v in VILLAGES.get(cell, [])]
                            if village not in valid_villages:
                                errors["village"] = [
                                    "Invalid village code for the selected cell"
                                ]

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def validate_province(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        valid_provinces = [p[0] for p in PROVINCES]
        if value not in valid_provinces:
            raise serializers.ValidationError("Invalid province code")
        return value

    def validate_district(self, value):
        # Check if district code exists in DISTRICTS for the given province
        province_code = self.initial_data.get("province")
        valid_districts = [d[0] for d in DISTRICTS.get(province_code, [])]
        if value not in valid_districts:
            raise serializers.ValidationError("Invalid district code")
        return value

    def validate_sector(self, value):
        # Check if sector code exists in SECTORS for the given district
        district_code = self.initial_data.get("district")
        valid_sectors = [s[0] for s in SECTORS.get(district_code, [])]
        if value not in valid_sectors:
            raise serializers.ValidationError("Invalid sector code")
        return value

    def validate_cell(self, value):
        # Check if cell code exists in CELLS for the given sector
        sector_code = self.initial_data.get("sector")
        valid_cells = [c[0] for c in CELLS.get(sector_code, [])]
        if value not in valid_cells:
            raise serializers.ValidationError("Invalid cell code")
        return value

    def validate_village(self, value):
        # Check if village code exists in VILLAGES for the given cell
        cell_code = self.initial_data.get("cell")
        valid_villages = [v[0] for v in VILLAGES.get(cell_code, [])]
        if value not in valid_villages:
            raise serializers.ValidationError("Invalid village code")
        return value


class ServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["service_name", "description"]


class FacilityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        fields = ["image", "caption", "image_type", "uploaded_at"]


class BulkFacilityImageSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        facility = self.context.get("facility")
        images = [FacilityImage(facility=facility, **item) for item in validated_data]
        created_images = FacilityImage.objects.bulk_create(images)
        return created_images


class FacilityImageBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityImage
        fields = ["image", "caption", "image_type"]
        list_serializer_class = BulkFacilityImageSerializer


class PopulationStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthFacilityPopulation
        exclude = ["facility"]


class FacilityFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityFees
        exclude = ["facility"]


class GovernmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentData
        exclude = ["facility"]


class AdvancedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedFacilityData
        exclude = ["facility"]


class ServicesSerializer(serializers.ModelSerializer):
    offered_services = ServiceDetailSerializer(many=True)  # Nested serializer

    def validate_special_programs(self, value):
        validate_special_programs(value)
        return value

    def validate_performance_metrics(self, value):
        validate_performance_metrics(value)
        return value

    class Meta:
        model = HealthFacilityServices
        exclude = ["facility"]

    def create(self, validated_data):
        offered_services_data = validated_data.pop("offered_services", [])
        health_facility_service = HealthFacilityServices.objects.create(
            **validated_data
        )

        # Handling ManyToMany relationship
        offered_services_instances = []
        for service_data in offered_services_data:
            service_instance, created = Service.objects.get_or_create(**service_data)
            offered_services_instances.append(service_instance)

        health_facility_service.offered_services.set(offered_services_instances)
        return health_facility_service


class ResourcesSerializer(serializers.ModelSerializer):
    def validate_laboratories(self, value):
        validate_laboratories(value)
        return value

    class Meta:
        model = FacilityResources
        fields = [
            "facility",
            "beds",
            "laboratories",
            "diagnostic_services",
            "ict_equipment",
            "pharmacy",
            "special_needs_support",
        ]
        read_only_fields = ["facility"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = [
            "facility",
            "phone",
            "whatsapp",
            "email",
            "website",
            "social_media",
        ]
        read_only_fields = ["facility"]

    def validate_phone(self, value):
        if not value.startswith("+250"):
            raise serializers.ValidationError(
                "Phone number must start with +250 (Rwanda country code)"
            )
        return value


class HealthFacilitySerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)
    services = ServicesSerializer(required=False)
    resources = ResourcesSerializer(required=False)
    contact_info = ContactSerializer(required=False)
    population_stats = PopulationStatsSerializer(many=True, required=False)
    fees = FacilityFeesSerializer(required=False)
    government_data = GovernmentDataSerializer(required=False)
    advanced_data = AdvancedDataSerializer(required=False)
    images = FacilityImageSerializer(many=True, required=False)

    class Meta:
        model = HealthFacility
        fields = "__all__"
        read_only_fields = ("facility_id",)

    def validate(self, data):
        if "facility_name" in data and len(data["facility_name"]) < 3:
            raise serializers.ValidationError(
                {"facility_name": ["Facility name must be at least 3 characters long"]}
            )

        if self.instance is None:  # Only for creation
            facility_name = data.get("facility_name")
            if HealthFacility.objects.filter(
                facility_name__iexact=facility_name
            ).exists():
                raise serializers.ValidationError(
                    {"facility_name": ["A facility with this name already exists"]}
                )

        return data


class HealthFacilityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthFacility
        fields = [
            "facility_name",
            "facility_type",
            "level",
            "ownership",
            "average_rating",
            "verified",
            "verified_by",
        ]

    def validate(self, data):
        """Custom validation for creating a health facility"""
        if "facility_name" in data and len(data["facility_name"]) < 3:
            raise serializers.ValidationError(
                {"facility_name": ["Facility name must be at least 3 characters long"]}
            )

        # facility_name = data.get("facility_name")
        # if HealthFacility.objects.filter(facility_name__iexact=facility_name).exists():
        #     raise serializers.ValidationError(
        #         {"facility_name": ["A facility with this name already exists"]}
        #     )

        return data


class HealthFacilityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthFacility
        fields = [
            "facility_name",
            "facility_type",
            "level",
            "ownership",
            "average_rating",
            "verified",
            "verified_by",
        ]
        extra_kwargs = {
            "facility_name": {"required": False},
            "facility_type": {"required": False},
            "level": {"required": False},
            "ownership": {"required": False},
            "average_rating": {"required": False},
            "verified": {"required": False},
            "verified_by": {"required": False},
        }

    def validate(self, data):
        """Custom validation for updating a health facility"""
        if "facility_name" in data and len(data["facility_name"]) < 3:
            raise serializers.ValidationError(
                {"facility_name": ["Facility name must be at least 3 characters long"]}
            )

        return data
