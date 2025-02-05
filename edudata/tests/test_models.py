from django.test import TestCase
from edudata.models import (
    School,
    SchoolLocation,
    SchoolFees,
    SchoolContact,
    SchoolImage,
    AlumniNetwork,
    SchoolGovernmentData,
    AdmissionPolicy,
)
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
from edudata.serializers import SchoolLocationSerializer
from rest_framework.exceptions import ValidationError


class SchoolTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create a single school instance to be shared across all test cases"""
        cls.school = School.objects.create(
            school_id="101010",
            school_name="Test School",
            school_type="DAY",
            school_level="SECONDARY",
            school_gender="MF",
            school_ownership="PRIVATE",
            average_rating=4.5,
            review_count=10,
            school_description="Test description",
        )


class SchoolModelTests(SchoolTestBase):
    def test_school_creation(self):
        """Test school instance creation"""
        self.assertEqual(self.school.school_name, "Test School")
        self.assertEqual(self.school.school_type, "DAY")
        self.assertEqual(str(self.school), "Test School")

    def test_school_fields_validation(self):
        """Test field validations"""
        self.assertEqual(self.school.average_rating, 4.5)
        self.assertEqual(self.school.review_count, 10)


class SchoolLocationModelTests(SchoolTestBase):
    @classmethod
    def setUpTestData(cls):
        """Create location using the already existing school"""
        super().setUpTestData()
        cls.location = SchoolLocation.objects.create(
            school=cls.school,
            province="RW.KG",
            district="RW.KG.NY",
            sector="RW.KG.NY.GT",
            cell="RW.KG.NY.GT.AK",
            village="RW.KG.NY.GT.AK.GH",
            address="Test Address",
            latitude=-1.9441,
            longitude=30.0619,
        )

    def test_location_creation(self):
        """Test location instance creation"""
        self.assertEqual(self.location.province, "RW.KG")
        self.assertEqual(self.location.address, "Test Address")

    def test_location_coordinates_validation(self):
        """Test coordinate validation"""
        invalid_data = {
            "school": self.school,
            "latitude": 91,
            "longitude": 181,
        }
        serializer = SchoolLocationSerializer(data=invalid_data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class SchoolFeesModelTests(SchoolTestBase):
    @classmethod
    def setUpTestData(cls):
        """Create fees using the already existing school"""
        super().setUpTestData()
        cls.fees = SchoolFees.objects.create(
            school=cls.school, currency="RWF", amount=50000.00
        )

    def test_fees_creation(self):
        """Test fees instance creation"""
        self.assertEqual(self.fees.currency, "RWF")
        self.assertEqual(float(self.fees.amount), 50000.00)


class SchoolContactModelTests(SchoolTestBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.contact = SchoolContact.objects.create(
            school=cls.school,
            phone_number="+250788123456",
            email="test@example.com",
            website="https://www.example.com",
            social_media={
                "facebook": "https://www.facebook.com/tests",
                "twitter": "https://www.twitter.com/tests",
                "instagram": "https://www.instagram.com/tests",
            },
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.phone_number, "+250788123456")
        self.assertEqual(self.contact.email, "test@example.com")
        self.assertEqual(
            self.contact.social_media,
            {
                "facebook": "https://www.facebook.com/tests",
                "twitter": "https://www.twitter.com/tests",
                "instagram": "https://www.instagram.com/tests",
            },
        )

    def test_contact_fields_validation(self):
        self.assertEqual(self.contact.phone_number, "+250788123456")
        self.assertEqual(self.contact.email, "test@example.com")
        self.assertEqual(self.contact.website, "https://www.example.com")
        self.assertEqual(
            self.contact.social_media,
            {
                "facebook": "https://www.facebook.com/tests",
                "twitter": "https://www.twitter.com/tests",
                "instagram": "https://www.instagram.com/tests",
            },
        )


class SchoolImageModelTests(SchoolTestBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.school_image = SchoolImage.objects.create(
            school=cls.school,
            image=SimpleUploadedFile(
                "test_image.jpg", b"file_content", content_type="image/jpeg"
            ),
        )

    def test_school_image_creation(self):
        """Test creating a school image record"""

        self.assertEqual(SchoolImage.objects.count(), 1)
        self.assertEqual(self.school_image.school, self.school)
        self.assertTrue(
            self.school_image.image.name.startswith("school_images/testschool_photos/")
        )


class AlumniNetworkModelTests(SchoolTestBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.alumni_network = AlumniNetwork.objects.create(
            school=cls.school,
            notable_alumni={
                "name": "Jane Doe",
                "achievement": "Minister of Education",
            },
        )

    def test_alumni_network_creation(self):
        """Test creating an alumni network record"""
        self.assertEqual(self.alumni_network.school, self.school)
        self.assertEqual(
            self.alumni_network.notable_alumni,
            {"name": "Jane Doe", "achievement": "Minister of Education"},
        )


class SchoolGovernmentDataModelTests(SchoolTestBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.government_data = SchoolGovernmentData.objects.create(
            school=cls.school,
            government_supported=True,
            registration_date=datetime.date.today(),
            inspection_record={"date": "2022-08-01", "result": "Compliant"},
        )

    def test_government_data_creation(self):
        self.assertEqual(self.government_data.school, self.school)
        self.assertEqual(self.government_data.government_supported, True)
        self.assertEqual(
            self.government_data.inspection_record,
            {"date": "2022-08-01", "result": "Compliant"},
        )

    def test_government_data_fields_validation(self):
        self.assertEqual(self.government_data.school, self.school)
        self.assertEqual(self.government_data.government_supported, True)
        self.assertEqual(self.government_data.registration_date, datetime.date.today())
        self.assertEqual(
            self.government_data.inspection_record,
            {"date": "2022-08-01", "result": "Compliant"},
        )


class SchoolAdmissionPolicyModelTests(SchoolTestBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.admission_policy = AdmissionPolicy.objects.create(
            school=cls.school,
            admission_policy="SELECTIVE",
            discipline_policy="STRICT",
            parental_engagement="Once per term",
        )

    def test_admission_policy_creation(self):
        self.assertEqual(self.admission_policy.school, self.school)
        self.assertEqual(self.admission_policy.admission_policy, "SELECTIVE")
        self.assertEqual(self.admission_policy.discipline_policy, "STRICT")
        self.assertEqual(self.admission_policy.parental_engagement, "Once per term")
