from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from faker import Faker
import string
import random

User = get_user_model()
fake = Faker()


class UserTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")

        # Helper function to generate valid password
        def generate_valid_password():
            # Ensure password meets all criteria
            password = (
                random.choice(string.ascii_uppercase)  # Capital letter
                + random.choice(string.ascii_lowercase)  # Lowercase letter
                + random.choice(string.digits)  # Number
                + random.choice("!@#$%^&*()_+")  # Special character
                + "".join(
                    random.choices(
                        string.ascii_letters + string.digits + "!@#$%^&*()_+", k=4
                    )
                )  # Random additional chars
            )
            return password

        # Valid test data
        self.valid_password = generate_valid_password()
        self.valid_user_data = {
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": self.valid_password,
            "confirm_password": self.valid_password,
        }

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.valid_user_data["email"])

    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        # Create first user
        self.client.post(self.register_url, self.valid_user_data)

        # Try to create second user with same email
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_user_registration_invalid_email(self):
        """Test registration with invalid email"""
        invalid_data = self.valid_user_data.copy()
        invalid_data["email"] = "invalid-email"
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_names(self):
        """Test registration with invalid names"""
        # Test invalid first name
        invalid_data = self.valid_user_data.copy()
        invalid_data["first_name"] = "John123"
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid last name
        invalid_data = self.valid_user_data.copy()
        invalid_data["last_name"] = "Doe123"
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_password_validation(self):
        """Test registration with various invalid passwords"""
        test_cases = [
            ("short", "Password must be at least 8 characters long."),
            (
                "lowercase123!",
                "Password must contain at least one small and capital letter.",
            ),
            (
                "UPPERCASE123!",
                "Password must contain at least one small and capital letter.",
            ),
            ("NoNumbers!!", "Password must contain at least one numerical value."),
            ("NoSpecial123", "Password must contain at least one special character."),
        ]

        for password, expected_message in test_cases:
            invalid_data = self.valid_user_data.copy()
            invalid_data["password"] = password
            invalid_data["confirm_password"] = password
            response = self.client.post(self.register_url, invalid_data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("password", response.data)

    def test_user_login_success(self):
        """Test successful login"""
        # Create user first
        self.client.post(self.register_url, self.valid_user_data)

        # Attempt login
        login_data = {
            "email": self.valid_user_data["email"],
            "password": self.valid_user_data["password"],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        # Create user first
        self.client.post(self.register_url, self.valid_user_data)

        # Attempt login with wrong password
        login_data = {
            "email": self.valid_user_data["email"],
            "password": "Wrongpassword123!!",
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_model_str_method(self):
        """Test the string representation of the User model"""
        user = User.objects.create_user(
            email=self.valid_user_data["email"],
            password=self.valid_user_data["password"],
            first_name=self.valid_user_data["first_name"],
            last_name=self.valid_user_data["last_name"],
        )
        self.assertEqual(str(user), self.valid_user_data["email"])

    def test_required_fields_validation(self):
        """Test validation of required fields"""
        required_fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        ]

        for field in required_fields:
            invalid_data = self.valid_user_data.copy()
            invalid_data[field] = ""
            response = self.client.post(self.register_url, invalid_data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
