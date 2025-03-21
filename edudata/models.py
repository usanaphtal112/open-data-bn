from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import re as regex
from accounts.models import CustomUser


class SchoolChoices:
    class Type(models.TextChoices):
        BOARDING = "BOARDING", "Boarding School"
        DAY = "DAY", "Day School"
        BOARDING_AND_DAY = "BOTH", "Boarding and Day School"

    class Gender(models.TextChoices):
        BOYS = "M", "Boys Only"
        GIRLS = "F", "Girls Only"
        MIXED = "MF", "Mixed Gender"

    class Ownership(models.TextChoices):
        PUBLIC = "PUBLIC", "Public School"
        PRIVATE = "PRIVATE", "Private School"
        GOVERNMENT_AIDED = "GOVT_AIDED", "Government Aided"
        RELIGIOUS = "RELIGIOUS", "Religious Institution"
        INTERNATIONAL = "INTERNATIONAL", "International School"
        OTHER = "OTHER", "Other"

    class Level(models.TextChoices):
        KINDERGARTEN = "KINDERGARTEN", "Kindergarten"
        PRIMARY = "PRIMARY", "Primary School"
        SECONDARY = "SECONDARY", "Secondary School"
        COMBINED = "COMBINED", "Combined School"
        TVET = "TVET", "Technical and Vocational"
        TERTIARY = "TERTIARY", "Tertiary Institution"
        UNIVERSITY = "UNIVERSITY", "University"
        COLLEGE = "COLLEGE", "College"
        INSTITUTE = "INSTITUTE", "Institute"
        OTHER = "OTHER", "Other"

    class Admission(models.TextChoices):
        OPEN = "OPEN", "Open Admission"
        SELECTIVE = "SELECTIVE", "Selective Admission"
        MERIT_BASED = "MERIT", "Merit Based"
        INTERVIEW = "INTERVIEW", "Interview Required"
        ENTRANCE_EXAM = "EXAM", "Entrance Examination"
        OTHER = "OTHER", "Other"

    class Discipline(models.TextChoices):
        STRICT = "STRICT", "Strict"
        MODERATE = "MODERATE", "Moderate"
        LENIENT = "LENIENT", "Lenient"
        SELF_DISCIPLINE = "SELF", "Self-Disciplined"
        OTHER = "OTHER", "Other"

    class ImageType(models.TextChoices):
        EXTERIOR = "EXTERIOR", "Exterior"
        INTERIOR = "INTERIOR", "Interior"
        FACILITY = "FACILITY", "Facility"
        OTHER = "OTHER", "Other"


class School(models.Model):
    """
    This model represents a school in the database.
    """

    school_code = models.IntegerField(unique=True)
    school_name = models.CharField(max_length=500)
    school_type = models.CharField(
        max_length=100, choices=SchoolChoices.Type.choices, blank=True, null=True
    )
    school_level = models.CharField(
        max_length=100, choices=SchoolChoices.Level.choices, blank=True, null=True
    )
    school_gender = models.CharField(
        max_length=100,
        choices=SchoolChoices.Gender.choices,
        blank=True,
        null=True,
        default=SchoolChoices.Gender.MIXED,
    )
    school_ownership = models.CharField(
        max_length=100, choices=SchoolChoices.Ownership.choices, blank=True, null=True
    )
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True
    )
    review_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_schools",
    )
    school_description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_schools",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.school_name


class SchoolImage(models.Model):
    """
    This model represents an image of a school in the database.
    Multiple images can be stored for each school in a dedicated folder.
    """

    def school_image_path(instance, filename):
        # Sanitize school name for file path
        safe_school_name = regex.sub(
            r"[^\w\-_]", "", instance.school.school_name
        ).lower()  # Remove non-alphanumeric, replace spaces with underscores, and lowercase
        return f"school_images/{safe_school_name}_photos/{filename}"

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=school_image_path)
    caption = models.CharField(max_length=255, blank=True, null=True)
    image_type = models.CharField(
        max_length=15,
        choices=SchoolChoices.ImageType.choices,
        default=SchoolChoices.ImageType.OTHER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school.school_name} - {self.image.name}"


class SchoolLocation(models.Model):
    """
    This model represents a location of a school in the database.
    """

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    province = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    sector = models.CharField(max_length=50, blank=True, null=True)
    cell = models.CharField(max_length=50, blank=True, null=True)
    village = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True,
        null=True,
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.province} - {self.district}"


class SchoolFees(models.Model):
    """
    This model represents the fees of a school in the database.
    """

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    currency = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school.school_name} - {self.currency} {self.amount}"


class SchoolContact(models.Model):
    """
    This model represents the contact details of a school in the database.
    """

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    whatsapp = models.CharField(max_length=13, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    social_media = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school.school_name} - {self.phone_number}"


class AlumniNetwork(models.Model):
    """
    This model represents the alumni network of a school in the database.
    """

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    notable_alumni = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school.school_name} - {self.notable_alumni}"


class SchoolGovernmentData(models.Model):
    """
    This model represents the government data of a school in the database.
    """

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    government_supported = models.BooleanField(default=False)
    registration_date = models.DateField(blank=True, null=True)
    inspection_record = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school.school_name} - {self.government_supported}"


class AdmissionPolicy(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    admission_policy = models.CharField(
        max_length=100, choices=SchoolChoices.Admission.choices, blank=True, null=True
    )
    discipline_policy = models.CharField(
        max_length=100, choices=SchoolChoices.Discipline.choices, blank=True, null=True
    )
    parental_engagement = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school.school_name} - {self.admission_policy}"
