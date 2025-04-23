from datetime import datetime, timedelta

import jwt
import pytest
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

pytestmark = [pytest.mark.e2e]


@pytest.fixture
def auth_header(test_user):
    """Fixture to create a valid auth header with JWT token"""
    refresh = RefreshToken()
    refresh["user_id"] = test_user["_id"]
    token = str(refresh.access_token)
    return f"Bearer {token}"


@pytest.fixture
def expired_token(test_user):
    """Fixture to create an expired JWT token"""
    # Create a token that expired 1 hour ago
    payload = {
        "user_id": test_user["_id"],
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    token = jwt.encode(
        payload,
        settings.SIMPLE_JWT["SIGNING_KEY"],
        algorithm=settings.SIMPLE_JWT["ALGORITHM"],
    )
    return f"Bearer {token}"


class TestAuth:
    @pytest.mark.unit
    def test_successful_auth(self, api_client, auth_header):
        """Test happy path for authentication verification"""
        api_client.credentials(HTTP_AUTHORIZATION=auth_header)
        response = api_client.get("/auth/")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data
        assert response.data["message"] == "Authenticated"
        assert "X-USER-ROLE" in response

    @pytest.mark.unit
    def test_missing_auth_header(self, api_client):
        """Test auth with missing authorization header"""
        response = api_client.get("/auth/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "error" in response.data
        assert "Authorization header is missing" in response.data["error"]

    @pytest.mark.unit
    def test_invalid_token_format(self, api_client):
        """Test auth with invalid token format"""
        api_client.credentials(HTTP_AUTHORIZATION="Invalid-format")
        response = api_client.get("/auth/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.unit
    def test_expired_token(self, api_client, expired_token):
        """Test auth with expired token"""
        api_client.credentials(HTTP_AUTHORIZATION=expired_token)
        response = api_client.get("/auth/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.unit
    def test_nonexistent_user(self, api_client):
        """Test auth with token for non-existent user"""
        # Create token with a fake user ID
        refresh = RefreshToken()
        refresh["user_id"] = "000000000000000000000000"  # Non-existent ObjectId
        token = str(refresh.access_token)

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = api_client.get("/auth/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
