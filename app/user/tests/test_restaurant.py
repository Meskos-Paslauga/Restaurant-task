from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


RESTAURANT_URL = reverse("user:restaurant")
CREATE_RESTAURANT_URL = reverse("user:createrestaurant")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicRestaurantTests(TestCase):

    def test_retrieve_restaurant_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(RESTAURANT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_valid_restaurant_success(self):
        """Test creating restaurant with valid payload is successful"""
        payload = {
            "email": "test@gmail.com",
            "password": "testpass",
            "name": "Test Name"
        }
        res = self.client.post(CREATE_RESTAURANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_restaurant_exists(self):
        """Test restaurant already exists fail"""
        payload = {"email": "test@gmail.com", "password": "testpass"}
        create_user(**payload)

        res = self.client.post(CREATE_RESTAURANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {"email": "test@gmail.com", "password": "pw"}
        res = self.client.post(CREATE_RESTAURANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_non_restaurant_can_not_see_page(self):
        """Test that not restaurant can't see the restaurant page"""
        self.user = create_user(
            email="test@gmail.com",
            password="testpass",
            name="name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        res = self.client.get(RESTAURANT_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateEmployeeTests(TestCase):
    """Tests for restaurant users"""

    def setUp(self):
        self.user = create_user(
            email="test@gmail.com",
            password="testpass",
            name="name",
            is_restaurant=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """test retrieving profile for logged in restaurant"""
        res = self.client.get(RESTAURANT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email,
            "is_employee": self.user.is_employee,
            "is_restaurant": self.user.is_restaurant,
        })

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on the restaurant url"""
        res = self.client.post(RESTAURANT_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the restaurant profile for authenticated restaurant"""
        payload = {"name": "new name", "password": "newpassword213"}

        res = self.client.patch(RESTAURANT_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
