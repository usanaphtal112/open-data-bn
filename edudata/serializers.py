from rest_framework import serializers
from .models import (
    School,
    SchoolLocation,
    SchoolImage,
    SchoolFees,
    SchoolContact,
    AlumniNetwork,
    SchoolGovernmentData,
    AdmissionPolicy,
    SchoolChoices,
)
from .location_data import PROVINCES, DISTRICTS, SECTORS, CELLS, VILLAGES
from .validators import (
    validate_social_media,
    validate_notable_alumni,
    validate_inspection_record,
)
from django.conf import settings
from urllib.parse import urljoin


class ProvinceSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class DistrictSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class SectorSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class CellSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class VillageSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class SchoolLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolLocation
        fields = [
            "id",
            "school",
            "province",
            "district",
            "sector",
            "cell",
            "village",
            "address",
            "latitude",
            "longitude",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "province": {"required": True},
            "district": {"required": True},
            "sector": {"required": True},
            "cell": {"required": True},
            "village": {"required": True},
        }

    def validate(self, data):
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


class SchoolImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolImage
        fields = ["school", "image", "caption", "image_type"]


class MultipleSchoolImageSerializer(serializers.Serializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    captions = serializers.ListField(
        child=serializers.CharField(max_length=255, allow_blank=True), required=False
    )
    image_types = serializers.ListField(
        child=serializers.ChoiceField(choices=SchoolChoices.ImageType.choices),
        required=False,
    )

    def create(self, validated_data):
        school = validated_data["school"]
        images = validated_data["images"]
        captions = validated_data.get("captions", [])
        image_types = validated_data.get("image_types", [])

        image_objects = []
        for index, image in enumerate(images):
            caption = captions[index] if index < len(captions) else ""
            image_type = (
                image_types[index]
                if index < len(image_types)
                else SchoolChoices.ImageType.OTHER
            )

            image_objects.append(
                SchoolImage(
                    school=school, image=image, caption=caption, image_type=image_type
                )
            )

        return SchoolImage.objects.bulk_create(image_objects)


class SchoolFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFees
        fields = "__all__"


class SchoolContactSerializer(serializers.ModelSerializer):
    def validate_social_media(self, value):
        validate_social_media(value)
        return value

    class Meta:
        model = SchoolContact
        fields = "__all__"


class AlumniNetworkSerializer(serializers.ModelSerializer):
    def validate_notable_alumni(self, value):
        validate_notable_alumni(value)
        return value

    class Meta:
        model = AlumniNetwork
        fields = "__all__"


class SchoolGovernmentDataSerializer(serializers.ModelSerializer):
    def validate_inspection_record(self, value):
        validate_inspection_record(value)
        return value

    class Meta:
        model = SchoolGovernmentData
        fields = "__all__"


class AdmissionPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionPolicy
        fields = "__all__"


class SchoolListSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        source="schoolcontact_set.first.phone_number", read_only=True
    )
    whatsapp = serializers.CharField(
        source="schoolcontact_set.first.whatsapp", read_only=True
    )
    cover = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            "id",
            "school_code",
            "school_name",
            "school_type",
            "school_level",
            "school_gender",
            "school_ownership",
            "verified",
            "average_rating",
            "phone",
            "whatsapp",
            "cover",
        ]

    def get_cover(self, obj):
        """Retrieve the first image of the school and return the full URL."""
        request = self.context.get("request")
        image = obj.images.first()
        if image and image.image:
            image_url = image.image.url
            # If request is available, construct the full URL
            if request:
                return request.build_absolute_uri(image_url)
            # Fallback in case request is not available
            return urljoin(settings.MEDIA_URL, image_url)
        return None


class SchoolDetailSerializer(serializers.ModelSerializer):
    images = SchoolImageSerializer(many=True, read_only=True)
    location = SchoolLocationSerializer(
        source="schoollocation_set.first", read_only=True
    )
    fees = SchoolFeesSerializer(source="schoolfees_set.first", read_only=True)
    contact = SchoolContactSerializer(source="schoolcontact_set.first", read_only=True)
    alumni = AlumniNetworkSerializer(source="alumninetwork_set.first", read_only=True)
    government_data = SchoolGovernmentDataSerializer(
        source="schoolgovernmentdata_set.first", read_only=True
    )
    admission = AdmissionPolicySerializer(
        source="admissionpolicy_set.first", read_only=True
    )

    class Meta:
        model = School
        fields = [
            "id",
            "school_code",
            "school_name",
            "school_type",
            "school_level",
            "school_gender",
            "school_ownership",
            "average_rating",
            "review_count",
            "verified",
            "school_description",
            "images",
            "location",
            "fees",
            "contact",
            "alumni",
            "government_data",
            "admission",
        ]


class SchoolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "school_code",
            "school_name",
            "school_type",
            "school_level",
            "school_gender",
            "school_ownership",
            "school_description",
        ]

    def validate(self, data):
        """Custom validation for creating a school"""
        if "school_name" in data and len(data["school_name"]) < 3:
            raise serializers.ValidationError(
                {"school_name": ["School name must be at least 3 characters long"]}
            )

        # school_name = data.get("school_name")
        # if School.objects.filter(school_name__iexact=school_name).exists():
        #     raise serializers.ValidationError(
        #         {"school_name": ["A school with this name already exists"]}
        #     )

        return data

    def create(self, validated_data):
        try:
            # Add the current logged-in user to the validated data
            validated_data["created_by"] = self.context["request"].user
            return super().create(validated_data)
        except Exception as e:
            raise  # Re-raise the exception after logging it
