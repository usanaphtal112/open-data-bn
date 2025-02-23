from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .Serializers import (
    HealthFacilitySerializer,
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


# JSON field examples for Health Facility-related models
HEALTH_FACILITY_JSON_EXAMPLES = {
    "special_programs": {
        "summary": "Special healthcare programs offered",
        "example": [
            {
                "name": "Surgical Outreach Program",
                "description": "Mobile surgical services for rural areas",
            },
            {
                "name": "Diabetes Management Program",
                "description": "Support for diabetes patients",
            },
        ],
        "description": "List of special programs with names and descriptions",
    },
    "performance_metrics": {
        "summary": "Annual performance metrics",
        "example": {
            "2022": {
                "readmission_rate": 5.5,
                "average_wait_time": 16.0,
                "patient_satisfaction": 90.0,
            },
            "2023": {
                "readmission_rate": 5.2,
                "average_wait_time": 15.5,
                "patient_satisfaction": 91.5,
            },
        },
        "description": "Yearly metrics including readmission rates, wait times, and satisfaction scores",
    },
    "laboratories": {
        "summary": "Laboratory facilities and equipment",
        "example": {
            "equipment": ["Microscopes", "Centrifuges"],
            "pathology": True,
            "microbiology": True,
        },
        "description": "Laboratory equipment and capabilities",
    },
    "operating_hours": {
        "summary": "Facility operating hours",
        "example": {"opening": "7h00", "closing": "23h00"},
        "description": "Daily operating hours",
    },
    "additional_costs": {
        "summary": "Additional service costs",
        "example": {"imaging": 22000.0, "lab_tests": 11000.0},
        "description": "Costs for various medical services",
    },
    "funding_allocation": {
        "summary": "Government funding allocation",
        "example": {"2022": 470000000, "2023": 500000000},
        "description": "Annual government funding amounts",
    },
}


get_facility_lists = swagger_auto_schema(
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


get_facility_details = swagger_auto_schema(
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


create_facility_services_docs = swagger_auto_schema(
    operation_description="Create services information for a health facility",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["facility"],
        properties={
            "facility": openapi.Schema(type=openapi.TYPE_INTEGER),
            "special_programs": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="List of special programs",
                example=HEALTH_FACILITY_JSON_EXAMPLES["special_programs"]["example"],
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "description": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            "performance_metrics": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Annual performance metrics",
                example=HEALTH_FACILITY_JSON_EXAMPLES["performance_metrics"]["example"],
            ),
            "laboratories": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Laboratory facilities information",
                example=HEALTH_FACILITY_JSON_EXAMPLES["laboratories"]["example"],
                properties={
                    "equipment": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        },
    ),
    responses={201: "Services created successfully", 400: "Invalid input data"},
)

create_health_facility_docs = swagger_auto_schema(
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

update_health_facility_docs = swagger_auto_schema(
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

delete_health_facility_docs = swagger_auto_schema(
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

create_facility_location_docs = swagger_auto_schema(
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

get_facility_location_details_docs = swagger_auto_schema(
    operation_description="Get location details for a health facility",
    responses={
        200: LocationSerializer,
        404: "Health facility or location not found",
    },
)

update_facility_location_docs = swagger_auto_schema(
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

delete_facility_location_docs = swagger_auto_schema(
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

get_facility_services_details_docs = swagger_auto_schema(
    operation_description="Get services information for a health facility",
    responses={
        200: ServicesSerializer,
        404: "Health facility or services information not found",
    },
)

update_facility_services_docs = swagger_auto_schema(
    operation_description="Update services information for a health facility",
    request_body=ServicesSerializer,
    responses={
        200: ServicesSerializer,
        400: "Bad Request",
        404: "Health facility or services information not found",
    },
)

delete_facility_services_docs = swagger_auto_schema(
    operation_description="Delete services information for a health facility",
    responses={
        204: "No content",
        404: "Health facility or services information not found",
    },
)

create_facility_resources_docs = swagger_auto_schema(
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

get_facility_resources_details_docs = swagger_auto_schema(
    operation_description="Get resources details for a health facility",
    responses={
        200: ResourcesSerializer,
        404: "Health facility or resources not found",
    },
)

update_facility_resources_docs = swagger_auto_schema(
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

delete_facility_resources_docs = swagger_auto_schema(
    operation_description="Delete resources information for a health facility",
    responses={
        204: "No content",
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    },
)

create_facility_contactinfo_docs = swagger_auto_schema(
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

get_facility_contactinfo_details_docs = swagger_auto_schema(
    operation_description="Get contact information for a health facility",
    responses={
        200: ContactSerializer,
        404: "Health facility or contact information not found",
    },
)

update_facility_contactinfo_docs = swagger_auto_schema(
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

delete_facility_contactinfo_docs = swagger_auto_schema(
    operation_description="Delete contact information for a health facility",
    responses={
        204: "No content",
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    },
)

create_facility_population_docs = swagger_auto_schema(
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

get_facility_population_details_docs = swagger_auto_schema(
    operation_description="Get population statistics for a health facility",
    responses={
        200: PopulationStatsSerializer,
        404: "Health facility or population statistics not found",
    },
)

update_facility_population_docs = swagger_auto_schema(
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

delete_facility_population_docs = swagger_auto_schema(
    operation_description="Delete population statistics for a health facility",
    responses={
        204: "No content",
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    },
)

create_facility_fees_docs = swagger_auto_schema(
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

get_facility_fees_details_docs = swagger_auto_schema(
    operation_description="Get fee information for a health facility",
    responses={
        200: FacilityFeesSerializer,
        404: "Health facility or fee information not found",
    },
)

update_facility_fees_docs = swagger_auto_schema(
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

delete_facility_fees_docs = swagger_auto_schema(
    operation_description="Delete fee information for a health facility",
    responses={
        204: "No content",
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    },
)

create_facility_governmentdata_docs = swagger_auto_schema(
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

get_facility_governmentdata_details_docs = swagger_auto_schema(
    operation_description="Get government data for a health facility",
    responses={
        200: GovernmentDataSerializer,
        404: "Health facility or government data not found",
    },
)


update_facility_governmentdata_docs = swagger_auto_schema(
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

delete_facility_governmentdata_docs = swagger_auto_schema(
    operation_description="Delete government data for a health facility",
    responses={
        204: "No content",
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    },
)

create_facility_advanceddata_docs = swagger_auto_schema(
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

get_facility_advanceddata_details_docs = swagger_auto_schema(
    operation_description="Get advanced data for a health facility",
    responses={
        200: AdvancedDataSerializer,
        404: "Health facility or advanced data not found",
    },
)

update_facility_advanceddata_docs = swagger_auto_schema(
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

delete_facility_advanceddata_docs = swagger_auto_schema(
    operation_description="Delete advanced data for a health facility",
    responses={
        204: "No content",
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    },
)

create_facility_images_docs = swagger_auto_schema(
    operation_description="Bulk upload images for a health facility",
    request_body=FacilityImageBulkSerializer(many=True),
    responses={
        201: FacilityImageBulkSerializer(many=True),
        400: "Bad Request",
        404: "Health Facility Not Found",
    },
)

get_facility_images_details_docs = swagger_auto_schema(
    operation_description="Get an image for a health facility",
    responses={
        200: FacilityImageSerializer,
        404: "Health facility or image not found",
    },
)

update_facility_images_docs = swagger_auto_schema(
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

delete_facility_images_docs = swagger_auto_schema(
    operation_description="Delete an image for a health facility",
    responses={
        204: "No content",
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
    },
)
