from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    SchoolDetailSerializer,
    SchoolLocationSerializer,
    SchoolListSerializer,
    SchoolCreateSerializer,
    MultipleSchoolImageSerializer,
    SchoolFeesSerializer,
    AdmissionPolicySerializer,
)
from .models import SchoolChoices


# JSON field examples for School-related models
SCHOOL_JSON_EXAMPLES = {
    "social_media": {
        "summary": "Social media links for the school",
        "example": {
            "twitter": "https://twitter.com/LyceeDeKigali",
            "youtube": "https://youtube.com/LyceeDeKigali",
            "facebook": "https://facebook.com/LyceeDeKigali",
            "linkedin": "https://linkedin.com/LyceeDeKigali",
            "instagram": "https://instagram.com/LyceeDeKigali",
        },
        "description": "Dictionary containing social media platform URLs. All URLs must start with 'https://'.",
    },
    "notable_alumni": {
        "summary": "List of notable alumni and their achievements",
        "example": [
            {"name": "Jean de Dieu Uwihanganye", "achievement": "Renowned Politician"},
            {"name": "Marie Claire Uwimana", "achievement": "Award-winning Journalist"},
        ],
        "description": "List of objects containing alumni names and their achievements",
    },
    "inspection_record": {
        "summary": "School inspection records",
        "example": [
            {"date": "2022-05-01", "result": "Compliant"},
            {"date": "2021-04-15", "result": "Compliant"},
        ],
        "description": "List of inspection records with dates in YYYY-MM-DD format",
    },
}


get_province_docs = swagger_auto_schema(
    operation_description="Get list of all provinces",
    responses={
        200: openapi.Response(
            description="List of provinces retrieved successfully",
            examples={"application/json": [{"code": "RW.KG", "name": "KIGALI CITY"}]},
        )
    },
)


get_district_docs = swagger_auto_schema(
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


get_sector_docs = swagger_auto_schema(
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
            examples={"application/json": [{"code": "RW.KG.NY.GT", "name": "GITEGA"}]},
        ),
        400: openapi.Response(
            description="Bad Request - Invalid or missing district_code",
            examples={"application/json": {"error": "district_code is required"}},
        ),
    },
)


get_cell_docs = swagger_auto_schema(
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
                "application/json": [{"code": "RW.KG.NY.GT.AK", "name": "AKABAHIZI"}]
            },
        ),
        400: openapi.Response(
            description="Bad Request - Invalid or missing sector_code",
            examples={"application/json": {"error": "sector_code is required"}},
        ),
    },
)


get_village_docs = swagger_auto_schema(
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
                "application/json": [{"code": "RW.KG.NY.GT.AK.GH", "name": "GIHANGA"}]
            },
        ),
        400: openapi.Response(
            description="Bad Request - Invalid or missing cell_code",
            examples={"application/json": {"error": "cell_code is required"}},
        ),
    },
)

get_school_lists_docs = swagger_auto_schema(
    operation_description="Get list of all schools",
    responses={200: SchoolListSerializer, 404: "School not found"},
)

filter_school_by_location_docs = swagger_auto_schema(
    operation_description="Filter schools by location codes (independent)",
    manual_parameters=[
        openapi.Parameter(
            "province",
            openapi.IN_QUERY,
            description="Province code (e.g., 'RW.KL')",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "district",
            openapi.IN_QUERY,
            description="District code (e.g., 'RW.KL.GB')",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "sector",
            openapi.IN_QUERY,
            description="Sector code (e.g., 'RW.KL.GB.KI')",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "cell",
            openapi.IN_QUERY,
            description="Cell code (e.g., 'RW.KL.GB.KI.KR')",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "village",
            openapi.IN_QUERY,
            description="Village code (e.g., 'RW.KL.GB.KI.KR.AM')",
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: SchoolDetailSerializer(many=True),
        400: "Invalid location code",
    },
)


filter_school_by_location_hierarchical_docs = swagger_auto_schema(
    operation_description="Filter schools by location codes (hierarchical)",
    manual_parameters=[
        openapi.Parameter(
            "province",
            openapi.IN_QUERY,
            description="Province code (e.g., 'RW.KL')",
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            "district",
            openapi.IN_QUERY,
            description="District code (e.g., 'RW.KL.GB')",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "sector",
            openapi.IN_QUERY,
            description="Sector code (e.g., 'RW.KL.GB.KI')",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "cell",
            openapi.IN_QUERY,
            description="Cell code (e.g., 'RW.KL.GB.KI.KR')",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "village",
            openapi.IN_QUERY,
            description="Village code (e.g., 'RW.KL.GB.KI.KR.AM')",
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: SchoolDetailSerializer(many=True),
        400: "Invalid location hierarchy",
    },
)


get_school_filters_docs = swagger_auto_schema(
    operation_description="Get all possible filter options for schools",
    responses={
        200: openapi.Response(
            description="Filter options retrieved successfully",
            examples={
                "application/json": {
                    "ownership_types": [
                        {"value": "PUBLIC", "label": "Public School"},
                        {"value": "PRIVATE", "label": "Private School"},
                    ],
                    "school_levels": [
                        {"value": "PRIMARY", "label": "Primary School"},
                        {"value": "SECONDARY", "label": "Secondary School"},
                    ],
                    # ... other choices
                }
            },
        )
    },
)


# Get School Filters
filter_school_docs = swagger_auto_schema(
    operation_description="Filter schools by their characteristics",
    manual_parameters=[
        openapi.Parameter(
            "ownership",
            openapi.IN_QUERY,
            description=f"School ownership type. Choices: {[choice[0] for choice in SchoolChoices.Ownership.choices]}",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "level",
            openapi.IN_QUERY,
            description=f"School level. Choices: {[choice[0] for choice in SchoolChoices.Level.choices]}",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "gender",
            openapi.IN_QUERY,
            description=f"School gender type. Choices: {[choice[0] for choice in SchoolChoices.Gender.choices]}",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "type",
            openapi.IN_QUERY,
            description=f"School type. Choices: {[choice[0] for choice in SchoolChoices.Type.choices]}",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "admission",
            openapi.IN_QUERY,
            description=f"Admission policy. Choices: {[choice[0] for choice in SchoolChoices.Admission.choices]}",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "discipline",
            openapi.IN_QUERY,
            description=f"Discipline policy. Choices: {[choice[0] for choice in SchoolChoices.Discipline.choices]}",
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: SchoolDetailSerializer(many=True),
        400: "Invalid filter parameters",
    },
)

# Create School Location

create_school_location_docs = swagger_auto_schema(
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


get_school_details_docs = swagger_auto_schema(
    operation_description="Get detailed information about a specific school",
    responses={
        200: openapi.Response(
            description="School details retrieved successfully",
            examples={
                "application/json": {
                    "contact": {
                        "social_media": SCHOOL_JSON_EXAMPLES["social_media"]["example"]
                    },
                    "alumni": {
                        "notable_alumni": SCHOOL_JSON_EXAMPLES["notable_alumni"][
                            "example"
                        ]
                    },
                    "government_data": {
                        "inspection_record": SCHOOL_JSON_EXAMPLES["inspection_record"][
                            "example"
                        ]
                    },
                }
            },
        ),
        404: "School not found",
    },
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

create_school_docs = swagger_auto_schema(
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
# School Contact Create Documentation
create_school_contact_docs = swagger_auto_schema(
    operation_description="Create contact information for a school",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["school", "phone_number"],
        properties={
            "school": openapi.Schema(type=openapi.TYPE_INTEGER),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING, max_length=13),
            "whatsapp": openapi.Schema(type=openapi.TYPE_STRING, max_length=13),
            "email": openapi.Schema(type=openapi.TYPE_STRING, format="email"),
            "website": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
            "social_media": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Social media links dictionary",
                example=SCHOOL_JSON_EXAMPLES["social_media"]["example"],
                properties={
                    "twitter": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                    "facebook": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                    "instagram": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                    "linkedin": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                    "youtube": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                },
            ),
        },
    ),
    responses={201: "Contact created successfully", 400: "Invalid input data"},
)

# Alumni Network Create Documentation
create_alumni_network_docs = swagger_auto_schema(
    operation_description="Create alumni network information for a school",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["school"],
        properties={
            "school": openapi.Schema(type=openapi.TYPE_INTEGER),
            "notable_alumni": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="List of notable alumni and their achievements",
                example=SCHOOL_JSON_EXAMPLES["notable_alumni"]["example"],
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "achievement": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    ),
    responses={201: "Alumni network created successfully", 400: "Invalid input data"},
)

# School Government Data Create Documentation
create_school_government_data_docs = swagger_auto_schema(
    operation_description="Create government data for a school",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["school"],
        properties={
            "school": openapi.Schema(type=openapi.TYPE_INTEGER),
            "government_supported": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "registration_date": openapi.Schema(
                type=openapi.TYPE_STRING, format="date"
            ),
            "inspection_record": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="List of inspection records",
                example=SCHOOL_JSON_EXAMPLES["inspection_record"]["example"],
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                        "result": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    ),
    responses={201: "Government data created successfully", 400: "Invalid input data"},
)

create_school_image_docs = swagger_auto_schema(
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

create_school_fees_docs = swagger_auto_schema(
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

create_school_admission_policy_docs = swagger_auto_schema(
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
