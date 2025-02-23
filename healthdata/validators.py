from rest_framework.validators import ValidationError


def validate_special_programs(programs):
    """
    Validates special programs JSON structure.
    Expected format:
    [
        {
            "name": "string",
            "description": "string"
        }
    ]
    """
    if not isinstance(programs, list):
        raise ValidationError("Special programs must be a list")

    for program in programs:
        if not isinstance(program, dict):
            raise ValidationError("Each program must be a dictionary")

        required_fields = ["name", "description"]
        for field in required_fields:
            if field not in program:
                raise ValidationError(f"Missing required field '{field}' in program")
            if not isinstance(program[field], str):
                raise ValidationError(f"Field '{field}' must be a string")


def validate_performance_metrics(metrics):
    """
    Validates performance metrics JSON structure.
    Expected format:
    {
        "YYYY": {
            "readmission_rate": float,
            "average_wait_time": float,
            "patient_satisfaction": float
        }
    }
    """
    if not isinstance(metrics, dict):
        raise ValidationError("Performance metrics must be a dictionary")

    required_metrics = ["readmission_rate", "average_wait_time", "patient_satisfaction"]

    for year, data in metrics.items():
        if not year.isdigit() or len(year) != 4:
            raise ValidationError(f"Invalid year format: {year}")

        if not isinstance(data, dict):
            raise ValidationError(f"Metrics for year {year} must be a dictionary")

        for metric in required_metrics:
            if metric not in data:
                raise ValidationError(
                    f"Missing required metric '{metric}' for year {year}"
                )
            if not isinstance(data[metric], (int, float)):
                raise ValidationError(f"Metric '{metric}' must be a number")


def validate_laboratories(labs):
    """
    Validates the laboratories JSON structure.

    Expected JSON format:
    {
        "equipment": ["string", ...],
        // Other field other than "equipment" must have a boolean value.
    }

    Example:
    {
        "equipment": ["Microscope", "Centrifuge"],
        "pathology": true,
        "microbiology": false,
        "radiology": true
    }
    """

    if not isinstance(labs, dict):
        raise ValidationError("Laboratories must be a dictionary")

    # Validate the 'equipment' field.
    if "equipment" not in labs:
        raise ValidationError("Missing required field 'equipment'")
    if not isinstance(labs["equipment"], list):
        raise ValidationError("Field 'equipment' must be a list")
    for idx, item in enumerate(labs["equipment"]):
        if not isinstance(item, str):
            raise ValidationError(
                f"Item at index {idx} in 'equipment' must be a string"
            )

    # For all fields other than 'equipment', ensure the value is a boolean.
    for field, value in labs.items():
        if field == "equipment":
            continue
        if not isinstance(value, bool):
            raise ValidationError(f"Field '{field}' must be a boolean")
