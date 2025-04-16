import pytest
from rest_framework import status

pytestmark = [pytest.mark.e2e]


class TestSignup:
    @pytest.mark.unit
    def test_successful_signup(self, api_client):
        """Test happy path for user signup"""
        data = {
            "email": "new_user@example.com",
            "password": "secure_password123",
        }
        response = api_client.post("/signup/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "access" in response.data
        assert "refresh" in response.data

    @pytest.mark.unit
    def test_missing_email(self, api_client):
        """Test signup with missing email"""
        data = {
            "password": "secure_password123"
        }
        response = api_client.post("/signup/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "Email and password are required" in response.data["error"]

    @pytest.mark.unit
    def test_missing_password(self, api_client):
        """Test signup with missing password"""
        data = {
            "email": "user@example.com"
        }
        response = api_client.post("/signup/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "Email and password are required" in response.data["error"]

    @pytest.mark.unit
    def test_invalid_email_format(self, api_client):
        """Test signup with invalid email format"""
        data = {
            "email": "invalid_email",
            "password": "secure_password123"
        }
        response = api_client.post("/signup/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "Invalid email format" in response.data["error"]

    @pytest.mark.unit
    def test_duplicate_user(self, api_client, test_user):
        """Test signup with an email that already exists"""
        data = {
            "email": test_user["email"],
            "password": "some_password"
        }
        response = api_client.post("/signup/", data, format="json")

        assert response.status_code == status.HTTP_409_CONFLICT
        assert "error" in response.data
        assert "User already exists" in response.data["error"]
