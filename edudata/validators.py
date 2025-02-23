from rest_framework.exceptions import ValidationError
from .location_data import PROVINCES, DISTRICTS, SECTORS, CELLS, VILLAGES
from .models import SchoolChoices
from datetime import datetime


def validate_independent_location_codes(
    province=None, district=None, sector=None, cell=None, village=None
):
    """
    Validates location codes independently (non-hierarchical).
    Each code is validated for existence without checking parent-child relationships.
    """
    errors = {}

    if province and province not in [p[0] for p in PROVINCES]:
        errors["province"] = f"Invalid province code: {province}"

    if district:
        all_districts = [d[0] for districts in DISTRICTS.values() for d in districts]
        if district not in all_districts:
            errors["district"] = f"Invalid district code: {district}"

    if sector:
        all_sectors = [s[0] for sectors in SECTORS.values() for s in sectors]
        if sector not in all_sectors:
            errors["sector"] = f"Invalid sector code: {sector}"

    if cell:
        all_cells = [c[0] for cells in CELLS.values() for c in cells]
        if cell not in all_cells:
            errors["cell"] = f"Invalid cell code: {cell}"

    if village:
        all_villages = [v[0] for villages in VILLAGES.values() for v in villages]
        if village not in all_villages:
            errors["village"] = f"Invalid village code: {village}"

    if errors:
        raise ValidationError(errors)

    return True


def validate_hierarchical_location_codes(
    province=None, district=None, sector=None, cell=None, village=None
):
    """
    Validates location codes hierarchically.
    Each code is validated for existence and proper parent-child relationship.
    Province is required when using this validator.
    """
    errors = {}

    # Province is required
    if not province:
        raise ValidationError({"province": "Province code is required"})

    # Validate province
    if province not in [p[0] for p in PROVINCES]:
        errors["province"] = f"Invalid province code: {province}"
        raise ValidationError(errors)

    # Validate district if provided
    if district:
        valid_districts = [d[0] for d in DISTRICTS.get(province, [])]
        if district not in valid_districts:
            errors["district"] = f"Invalid district code for province {province}"

    # Validate sector if provided
    if sector:
        if not district:
            errors["sector"] = "District code is required when specifying sector"
        else:
            valid_sectors = [s[0] for s in SECTORS.get(district, [])]
            if sector not in valid_sectors:
                errors["sector"] = f"Invalid sector code for district {district}"

    # Validate cell if provided
    if cell:
        if not sector:
            errors["cell"] = "Sector code is required when specifying cell"
        else:
            valid_cells = [c[0] for c in CELLS.get(sector, [])]
            if cell not in valid_cells:
                errors["cell"] = f"Invalid cell code for sector {sector}"

    # Validate village if provided
    if village:
        if not cell:
            errors["village"] = "Cell code is required when specifying village"
        else:
            valid_villages = [v[0] for v in VILLAGES.get(cell, [])]
            if village not in valid_villages:
                errors["village"] = f"Invalid village code for cell {cell}"

    if errors:
        raise ValidationError(errors)

    return True


def validate_school_filters(
    ownership=None,
    level=None,
    gender=None,
    school_type=None,
    admission=None,
    discipline=None,
):
    """
    Validates school filter parameters against defined choices.
    """
    errors = {}

    if ownership and ownership not in [
        choice[0] for choice in SchoolChoices.Ownership.choices
    ]:
        errors[
            "ownership"
        ] = f"Invalid ownership type: {ownership}. Valid choices are: {[choice[0] for choice in SchoolChoices.Ownership.choices]}"

    if level and level not in [choice[0] for choice in SchoolChoices.Level.choices]:
        errors[
            "level"
        ] = f"Invalid school level: {level}. Valid choices are: {[choice[0] for choice in SchoolChoices.Level.choices]}"

    if gender and gender not in [choice[0] for choice in SchoolChoices.Gender.choices]:
        errors[
            "gender"
        ] = f"Invalid gender type: {gender}. Valid choices are: {[choice[0] for choice in SchoolChoices.Gender.choices]}"

    if school_type and school_type not in [
        choice[0] for choice in SchoolChoices.Type.choices
    ]:
        errors[
            "school_type"
        ] = f"Invalid school type: {school_type}. Valid choices are: {[choice[0] for choice in SchoolChoices.Type.choices]}"

    if admission and admission not in [
        choice[0] for choice in SchoolChoices.Admission.choices
    ]:
        errors[
            "admission"
        ] = f"Invalid admission type: {admission}. Valid choices are: {[choice[0] for choice in SchoolChoices.Admission.choices]}"

    if discipline and discipline not in [
        choice[0] for choice in SchoolChoices.Discipline.choices
    ]:
        errors[
            "discipline"
        ] = f"Invalid discipline type: {discipline}. Valid choices are: {[choice[0] for choice in SchoolChoices.Discipline.choices]}"

    if errors:
        raise ValidationError(errors)

    return True


def validate_social_media(social_media):
    """
    Validates social media JSON structure.
    Expected format:
    {
        "twitter": "https://twitter.com/...",
        "facebook": "https://facebook.com/...",
        "instagram": "https://instagram.com/...",
        "linkedin": "https://linkedin.com/...",
        "youtube": "https://youtube.com/..."
    }
    """
    if not isinstance(social_media, dict):
        raise ValidationError("Social media must be a dictionary")

    allowed_platforms = ["twitter", "facebook", "instagram", "linkedin", "youtube"]

    for platform, url in social_media.items():
        if platform not in allowed_platforms:
            raise ValidationError(f"Invalid social media platform: {platform}")
        if not isinstance(url, str) or not url.startswith("https://"):
            raise ValidationError(f"Invalid URL for {platform}")


def validate_notable_alumni(alumni_list):
    """
    Validates notable alumni JSON structure.
    Expected format:
    [
        {
            "name": "string",
            "achievement": "string"
        }
    ]
    """
    if not isinstance(alumni_list, list):
        raise ValidationError("Notable alumni must be a list")

    for alumni in alumni_list:
        if not isinstance(alumni, dict):
            raise ValidationError("Each alumni entry must be a dictionary")

        required_fields = ["name", "achievement"]
        for field in required_fields:
            if field not in alumni:
                raise ValidationError(
                    f"Missing required field '{field}' in alumni entry"
                )
            if not isinstance(alumni[field], str):
                raise ValidationError(f"Field '{field}' must be a string")


def validate_inspection_record(records):
    """
    Validates inspection record JSON structure.
    Expected format:
    [
        {
            "date": "YYYY-MM-DD",
            "result": "string"
        }
    ]
    """
    if not isinstance(records, list):
        raise ValidationError("Inspection records must be a list")

    for record in records:
        if not isinstance(record, dict):
            raise ValidationError("Each inspection record must be a dictionary")

        if "date" not in record or "result" not in record:
            raise ValidationError("Each record must have 'date' and 'result' fields")

        try:
            datetime.strptime(record["date"], "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Date must be in YYYY-MM-DD format")
