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
)
from .location_data import PROVINCES, DISTRICTS, SECTORS, CELLS, VILLAGES


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
        fields = ["image"]


class SchoolFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFees
        exclude = ["id", "school", "created_at", "updated_at"]


class SchoolContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolContact
        exclude = ["id", "school", "created_at", "updated_at"]


class AlumniNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniNetwork
        exclude = ["id", "school", "created_at", "updated_at"]


class SchoolGovernmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGovernmentData
        exclude = ["id", "school", "created_at", "updated_at"]


class AdmissionPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionPolicy
        exclude = ["id", "school", "created_at", "updated_at"]


class SchoolSerializer(serializers.ModelSerializer):
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
            "school_id",
            "school_name",
            "school_type",
            "school_level",
            "school_gender",
            "school_ownership",
            "average_rating",
            "review_count",
            "school_description",
            "images",
            "location",
            "fees",
            "contact",
            "alumni",
            "government_data",
            "admission",
        ]
