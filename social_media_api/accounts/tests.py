from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword123"
        )
        self.login_url = "/accounts/login/"
        self.register_url = "/accounts/register/"
        self.logout_url = "/accounts/logout/"  # Updated logout URL
        self.profile_url = f"/accounts/profile/{self.test_user.id}/"

    def test_user_logout(self):
        """Test for successful user logout."""
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        # Log in and retrieve the token
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get("token")

        # Verify token is present
        self.assertIsNotNone(token, "Login response does not contain a token.")

        # Set token in HTTP Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Test logout endpoint
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure token is invalidated (access profile should fail)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")  # Retest with old token
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_access(self):
        """Test for accessing user profile."""
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        token = login_response.data.get("token")
        self.assertIsNotNone(token, "Login response does not contain a token.")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.test_user.username)
