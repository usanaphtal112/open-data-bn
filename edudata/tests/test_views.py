from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from edudata.models import (
    School,
    SchoolLocation,
    SchoolFees,
    SchoolContact,
    SchoolImage,
)
from ..location_data import PROVINCES, DISTRICTS, SECTORS


class BaseAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create a single school instance to be shared across all test cases"""
        cls.school = School.objects.create(
            school_id="101011",
            school_name="Test School",
            school_type="DAY",
            school_level="SECONDARY",
            school_gender="MF",
            school_ownership="PRIVATE",
            average_rating=4.5,
            review_count=10,
            school_description="Test description",
        )


class DetailedSchoolViewTests(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up related data for detailed school view tests"""
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

        cls.fees = SchoolFees.objects.create(
            school=cls.school, currency="RWF", amount=50000.00
        )

        cls.contact = SchoolContact.objects.create(
            school=cls.school,
            phone_number="+250700000000",
            email="test@school.com",
            website="http://testschool.com",
            social_media={
                "facebook": "https://www.facebook.com/tests",
                "twitter": "https://www.twitter.com/tests",
                "instagram": "https://www.instagram.com/tests",
            },
        )

        cls.image = SchoolImage.objects.create(
            school=cls.school, image="test_image.jpg"
        )

        cls.url = reverse("school-detail", kwargs={"pk": cls.school.id})

    def test_get_school_details(self):
        """Test retrieving school details"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["school_name"], "Test School")
        self.assertEqual(response.data["location"]["province"], "RW.KG")
        self.assertEqual(response.data["fees"]["currency"], "RWF")
        self.assertEqual(response.data["contact"]["email"], "test@school.com")
        self.assertEqual(len(response.data["images"]), 1)

    def test_get_nonexistent_school(self):
        """Test retrieving non-existent school"""
        url = reverse("school-detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SchoolLocationTests(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up location-related test data"""
        super().setUpTestData()

        cls.valid_data = {
            "school": cls.school.id,
            "province": "RW.KL",
            "district": "RW.KL.NG",
            "sector": "RW.KL.NG.NU",
            "cell": "RW.KL.NG.NU.RW",
            "village": "RW.KL.NG.NU.RW.RP",
            "address": "123 Main Street",
            "latitude": -1.9396,
            "longitude": 30.0444,
        }

    def test_create_valid_school_location(self):
        """Test creating a valid school location"""
        url = reverse("school-location-create")
        response = self.client.post(url, self.valid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SchoolLocation.objects.count(), 1)
        self.assertEqual(
            SchoolLocation.objects.get().province, self.valid_data["province"]
        )

    def test_create_with_invalid_province(self):
        """Test location creation with invalid province"""
        invalid_data = {**self.valid_data, "province": "INVALID"}
        url = reverse("school-location-create")
        response = self.client.post(url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("province", response.data)


class LocationEndpointsTest(APITestCase):
    def test_get_provinces(self):
        url = reverse("provinces")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(PROVINCES))

        # Verify first province matches our data
        first_province = PROVINCES[0]
        self.assertEqual(response.data[0]["code"], first_province[0])
        self.assertEqual(response.data[0]["name"], first_province[1])

    def test_get_districts_without_province(self):
        url = reverse("districts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_districts_with_valid_province(self):
        province_code = PROVINCES[0][0]  # First province code
        url = reverse("districts") + f"?province_code={province_code}"
        response = self.client.get(url)

        expected_districts = DISTRICTS.get(province_code, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(expected_districts))

    def test_get_districts_with_invalid_province(self):
        url = reverse("districts") + "?province_code=INVALID"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_sectors(self):
        district_code = DISTRICTS[PROVINCES[0][0]][0][
            0
        ]  # First district of first province
        url = reverse("sectors") + f"?district_code={district_code}"
        response = self.client.get(url)

        expected_sectors = SECTORS.get(district_code, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(expected_sectors))
