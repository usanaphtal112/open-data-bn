from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import re as regex
import random
from accounts.models import CustomUser


class HealthChoices:
    class FacilityType(models.TextChoices):
        HOSPITAL = "HOSPITAL", "Hospital"
        SPECIALIZED_HOSPITAL = "SPECIALIZED_HOSPITAL", "Specialized Hospital"
        CLINIC = "CLINIC", "Clinic"
        DENTIST = "DENTIST", "Dentist"
        PHARMACY = "PHARMACY", "Pharmacy"
        HEALTH_CENTER = "HEALTH_CENTER", "Health Center"
        HEALTH_POST = "HEALTH_POST", "Health Post"
        DISPENSARY = "DISPENSARY", "Dispensary"
        MEDICAL_PRACTICE = "MEDICAL_PRACTICE", "Medical Practice"
        MEDICAL_CLINIC = "MEDICAL_CLINIC", "Medical Clinic"
        SPECIALIZED_CLINIC = "SPECIALIZED_CLINIC", "Specialized Clinic"
        POLYCLINIC = "POLYCLINIC", "Polyclinic"
        BIOMEDICAL_LABORATORY = "BIOMEDICAL_LABORATORY", "Biomedical Laboratory"
        ANTENATAL_CLINIC = "ANTENATAL_CLINIC", "Antenatal Clinic"
        NURSING_HOME = "NURSING_HOME", "Nursing Home"
        PHYSIO_THERAPY_CENTER = "PHYSIO_THERAPY_CENTER", "Physio-Therapy Center"
        DENTAL_CLINIC = "DENTAL_CLINIC", "Dental Clinic"
        OPHTHALMIC_CLINIC = "OPHTHALMIC_CLINIC", "Opthalmic Clinic"
        OPTOMETRIC_CLINIC = "OPTOMETRIC_CLINIC", "Optometric Clinic"
        OPHTHALMIC_SURGERY = "OPHTHALMIC_SURGERY", "Opthalmic Surgery"
        MEDICAL_IMMAGING_CENTER = "MEDICAL_IMMAGING_CENTER", "Medical Imaging Center"
        HEALTH_AGENCY = "HEALTH_AGENCY", "Health Agency"
        HEALTH_TRAINING_CENTER = "HEALTH_TRAINING_CENTER", "Health Training Center"
        HEALTH_CONSULTATION = "HEALTH_CONSULTATION", "Health Consultation"
        HEALTH_SCREENING = "HEALTH_SCREENING", "Health Screening"
        OTHER = "OTHER", "Other"

    class FacilityOwnership(models.TextChoices):
        GOVERNMENT = "GOVERNMENT", "Government"
        PRIVATE = "PRIVATE", "Private"
        FAITH_BASED = "FAITH_BASED", "Faith-Based Organization"
        NGO = "NGO", "Non-Governmental Organization"
        CHURCH = "CHURCH", "Church"
        OTHER = "OTHER", "Other"

    class FacilityLevel(models.TextChoices):
        PROVINCIAL_REFERRAL = "PROVINCIAL_REFERRAL", "Province Hospital"
        DISTRICT_REFERRAL = "DISTRICT_REFERRAL", "District Referral"
        REFERRAL = "REFERRAL", "Referral"
        DISTRICT = "DISTRICT", "District"
        COMMUNITY = "COMMUNITY", "Community"
        OTHER = "OTHER", "Other"

    class Accreditation(models.TextChoices):
        ACCREDITED = "ACCREDITED", "Accredited"
        PENDING = "PENDING", "Pending"
        EXPIRED = "EXPIRED", "Expired"
        REVOKED = "REVOKED", "Revoked"
        OTHER = "OTHER", "Other"

    class ImageType(models.TextChoices):
        EXTERIOR = "EXTERIOR", "Exterior"
        INTERIOR = "INTERIOR", "Interior"
        FACILITY = "FACILITY", "Facility"
        OTHER = "OTHER", "Other"


class HealthFacility(models.Model):
    facility_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(r"^RW\d{8}$", "Facility ID must be RW followed by 8 digits")
        ],
    )
    facility_name = models.CharField(max_length=255)
    facility_type = models.CharField(
        max_length=100, choices=HealthChoices.FacilityType.choices
    )
    level = models.CharField(
        max_length=100,
        choices=HealthChoices.FacilityLevel.choices,
        blank=True,
        null=True,
    )
    ownership = models.CharField(
        max_length=100, choices=HealthChoices.FacilityOwnership.choices
    )

    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True
    )
    review_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="health_facility_verifier",
        null=True,
        blank=True,
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.facility_name} ({self.facility_code})"

    @staticmethod
    def generate_facility_code():
        """
        Generates a random facility ID in the format RW#####.
        """
        # Generate a random 5-digit number
        random_number = random.randint(10000000, 99999999)
        return f"RW{random_number}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a facility ID if it doesn't exist.
        """
        if not self.facility_code:
            self.facility_code = self.generate_facility_code()
            # Ensure the generated ID is unique
            while HealthFacility.objects.filter(
                facility_code=self.facility_code
            ).exists():
                self.facility_id = self.generate_facility_code()
        super().save(*args, **kwargs)


class HealthFacilityRating(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="rating_user"
    )
    facility = models.ForeignKey(
        HealthFacility, on_delete=models.CASCADE, related_name="rating_facility"
    )
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        null=True,
        blank=True,
    )


class HealthFacilityLocation(models.Model):
    facility = models.OneToOneField(
        HealthFacility, on_delete=models.CASCADE, related_name="location"
    )
    address = models.CharField(max_length=255)
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    sector = models.CharField(max_length=50, blank=True, null=True)
    cell = models.CharField(max_length=50, blank=True, null=True)
    village = models.CharField(max_length=50, blank=True, null=True)
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

    class Meta:
        verbose_name = "Facility Location"


class Service(models.Model):
    service_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.service_name


class HealthFacilityServices(models.Model):
    facility = models.OneToOneField(
        HealthFacility, on_delete=models.CASCADE, related_name="services"
    )
    offered_services = models.ManyToManyField(Service)
    special_programs = models.JSONField(default=list)
    performance_metrics = models.JSONField(default=dict)
    accreditation_status = models.CharField(
        max_length=30, choices=HealthChoices.Accreditation.choices
    )
    operating_hours = models.JSONField(default=dict, blank=True, null=True)
    emergency_services = models.BooleanField(default=True)
    languages_spoken = models.JSONField(default=list, blank=True, null=True)


class FacilityResources(models.Model):
    facility = models.OneToOneField(
        HealthFacility, on_delete=models.CASCADE, related_name="resources"
    )
    beds = models.PositiveIntegerField(default=0)
    laboratories = models.JSONField(default=dict)  # {type: bool, equipment: list}
    diagnostic_services = models.JSONField(default=list)
    ict_equipment = models.JSONField(default=dict)  # {computers: int, internet: bool}
    pharmacy = models.JSONField(default=dict)  # {available: bool, type: str}
    special_needs_support = models.BooleanField(default=False)


class HealthFacilityPopulation(models.Model):
    facility = models.ForeignKey(
        HealthFacility, on_delete=models.CASCADE, related_name="population_stats"
    )
    year = models.PositiveIntegerField()
    total_patients = models.PositiveIntegerField()
    male_patients = models.PositiveIntegerField()
    female_patients = models.PositiveIntegerField()
    total_staff = models.PositiveIntegerField()
    doctors = models.PositiveIntegerField()
    nurses = models.PositiveIntegerField()
    other_staff = models.PositiveIntegerField()

    class Meta:
        unique_together = ("facility", "year")


class FacilityFees(models.Model):
    facility = models.OneToOneField(
        HealthFacility, on_delete=models.CASCADE, related_name="fees"
    )
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    additional_costs = models.JSONField(default=dict)  # {service: cost}
    insurance_accepted = models.BooleanField(default=False)
    insurance_providers = models.JSONField(default=list)


class ContactInformation(models.Model):
    facility = models.OneToOneField(
        HealthFacility, on_delete=models.CASCADE, related_name="contact_info"
    )
    phone = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    social_media = models.JSONField(default=dict)  # {platform: url}


class GovernmentData(models.Model):
    facility = models.OneToOneField(
        HealthFacility, on_delete=models.CASCADE, related_name="government_data"
    )
    registration_date = models.DateField()
    government_support = models.BooleanField(default=False)
    inspection_records = models.JSONField(
        default=list
    )  # List of {date: str, result: str}
    funding_allocation = models.JSONField(default=dict)


class AdvancedFacilityData(models.Model):
    facility = models.OneToOneField(
        HealthFacility, on_delete=models.CASCADE, related_name="advanced_data"
    )
    nearby_facilities = models.JSONField(default=list)
    events = models.JSONField(default=list)
    partnerships = models.JSONField(default=list)


class FacilityImage(models.Model):
    def facility_image_path(instance, filename):
        # Sanitize Health facility name for file path
        safe_facility_name = regex.sub(
            r"[^\w\-_]", "", instance.facility.facility_name
        ).lower()  # Remove non-alphanumeric, replace spaces with underscores, and lowercase
        return f"Health_Facility_images/{safe_facility_name}_photos/{filename}"

    facility = models.ForeignKey(
        HealthFacility, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=facility_image_path)
    caption = models.CharField(max_length=255, blank=True, null=True)
    image_type = models.CharField(
        max_length=30,
        choices=HealthChoices.ImageType.choices,
        default=HealthChoices.ImageType.OTHER,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.facility.facility_name}"
