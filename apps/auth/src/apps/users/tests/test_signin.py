import pytest
from rest_framework import status

pytestmark = [pytest.mark.e2e]


class TestSignin:
    @pytest.mark.unit
    def test_successful_signin(self, api_client, test_user):
        """Test happy path for user signin"""
        data = {
            "email": test_user["email"],
            "password": "test_password",  # Matches the password in test_user fixture
        }
        response = api_client.post("/signin/", data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    @pytest.mark.unit
    def test_missing_credentials(self, api_client):
        """Test signin with missing credentials"""
        # Missing both email and password
        response = api_client.post("/signin/", {}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "Missing required fields" in response.data["error"]

    @pytest.mark.unit
    def test_user_not_found(self, api_client):
        """Test signin with non-existent user"""
        data = {"email": "nonexistent@example.com", "password": "some_password"}
        response = api_client.post("/signin/", data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data
        assert "User not found" in response.data["error"]

    @pytest.mark.unit
    def test_invalid_password(self, api_client, test_user):
        """Test signin with incorrect password"""
        data = {"email": test_user["email"], "password": "wrong_password"}
        response = api_client.post("/signin/", data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "error" in response.data
        assert "Invalid password" in response.data["error"]
