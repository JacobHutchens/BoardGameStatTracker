"""
Tests for authentication endpoints.
"""
import pytest
import requests
from conftest import make_authenticated_request, validate_response_shape


class TestAuthLogin:
    """Tests for POST /auth/login"""
    
    def test_login_success(self, http_client, base_url):
        """Test successful user login with valid credentials."""
        email = pytest.importorskip("os").getenv("TEST_USER_EMAIL")
        password = pytest.importorskip("os").getenv("TEST_USER_PASSWORD")
        
        if not email or not password:
            pytest.skip("TEST_USER_EMAIL and TEST_USER_PASSWORD must be set")
        
        response = http_client.post(
            f"{base_url}/auth/login",
            json={"emailOrUsername": email, "password": password}
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["accessToken", "refreshToken", "expiresIn", "user"],
            {
                "user.id": int,
                "user.username": str,
                "user.email": str,
                "user.designer": bool,
                "accessToken": str,
                "refreshToken": str,
                "expiresIn": int
            }
        )
    
    def test_login_invalid_credentials(self, http_client, base_url):
        """Test login with invalid credentials returns 401."""
        response = http_client.post(
            f"{base_url}/auth/login",
            json={"emailOrUsername": "invalid@example.com", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
    
    def test_login_missing_fields(self, http_client, base_url):
        """Test login with missing fields returns 400."""
        response = http_client.post(
            f"{base_url}/auth/login",
            json={"emailOrUsername": "test@example.com"}
        )
        
        assert response.status_code == 400


class TestAuthRegister:
    """Tests for POST /auth/register"""
    
    def test_register_success(self, http_client, base_url):
        """Test successful user registration."""
        import random
        import string
        
        # Generate unique username/email
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        username = f"testuser_{random_suffix}"
        email = f"test_{random_suffix}@example.com"
        password = "TestPassword123!"
        
        response = http_client.post(
            f"{base_url}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        
        assert response.status_code == 201
        data = response.json()
        validate_response_shape(
            response,
            ["accessToken", "refreshToken", "expiresIn", "user"],
            {
                "user.id": int,
                "user.username": str,
                "user.email": str,
                "user.designer": bool
            }
        )
        assert data["user"]["username"] == username
        assert data["user"]["email"] == email
    
    def test_register_duplicate_username(self, http_client, base_url):
        """Test registration with duplicate username returns 409."""
        # First registration
        username = "duplicate_test_user"
        email1 = "test1@example.com"
        password = "TestPassword123!"
        
        http_client.post(
            f"{base_url}/auth/register",
            json={"username": username, "email": email1, "password": password}
        )
        
        # Attempt duplicate username
        email2 = "test2@example.com"
        response = http_client.post(
            f"{base_url}/auth/register",
            json={"username": username, "email": email2, "password": password}
        )
        
        assert response.status_code == 409
    
    def test_register_duplicate_email(self, http_client, base_url):
        """Test registration with duplicate email returns 409."""
        email = "duplicate_email@example.com"
        password = "TestPassword123!"
        
        # First registration
        http_client.post(
            f"{base_url}/auth/register",
            json={"username": "user1", "email": email, "password": password}
        )
        
        # Attempt duplicate email
        response = http_client.post(
            f"{base_url}/auth/register",
            json={"username": "user2", "email": email, "password": password}
        )
        
        assert response.status_code == 409
    
    def test_register_missing_fields(self, http_client, base_url):
        """Test registration with missing fields returns 400."""
        response = http_client.post(
            f"{base_url}/auth/register",
            json={"username": "testuser"}
        )
        
        assert response.status_code == 400


class TestAuthPublisherLogin:
    """Tests for POST /auth/publisher/login"""
    
    def test_publisher_login_success(self, http_client, base_url):
        """Test successful publisher login."""
        email = pytest.importorskip("os").getenv("TEST_PUBLISHER_EMAIL")
        password = pytest.importorskip("os").getenv("TEST_PUBLISHER_PASSWORD")
        
        if not email or not password:
            pytest.skip("TEST_PUBLISHER_EMAIL and TEST_PUBLISHER_PASSWORD must be set")
        
        response = http_client.post(
            f"{base_url}/auth/publisher/login",
            json={"emailOrUsername": email, "password": password}
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["accessToken", "refreshToken", "expiresIn", "publisher"],
            {
                "publisher.id": int,
                "publisher.name": str,
                "accessToken": str,
                "refreshToken": str,
                "expiresIn": int
            }
        )
    
    def test_publisher_login_invalid_credentials(self, http_client, base_url):
        """Test publisher login with invalid credentials returns 401."""
        response = http_client.post(
            f"{base_url}/auth/publisher/login",
            json={"emailOrUsername": "invalid@example.com", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401


class TestAuthRefresh:
    """Tests for POST /auth/refresh"""
    
    def test_refresh_success(self, http_client, base_url, user_token):
        """Test successful token refresh."""
        if not user_token:
            pytest.skip("User token required")
        
        # Get refresh token from login
        email = pytest.importorskip("os").getenv("TEST_USER_EMAIL")
        password = pytest.importorskip("os").getenv("TEST_USER_PASSWORD")
        
        login_response = http_client.post(
            f"{base_url}/auth/login",
            json={"emailOrUsername": email, "password": password}
        )
        refresh_token = login_response.json().get("refreshToken")
        
        response = http_client.post(
            f"{base_url}/auth/refresh",
            json={"refreshToken": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["accessToken", "expiresIn"],
            {
                "accessToken": str,
                "expiresIn": int
            }
        )
    
    def test_refresh_invalid_token(self, http_client, base_url):
        """Test refresh with invalid token returns 401."""
        response = http_client.post(
            f"{base_url}/auth/refresh",
            json={"refreshToken": "invalid_refresh_token"}
        )
        
        assert response.status_code == 401


class TestAuthForgotPassword:
    """Tests for POST /auth/forgot-password"""
    
    def test_forgot_password_success(self, http_client, base_url):
        """Test forgot password request returns 200."""
        response = http_client.post(
            f"{base_url}/auth/forgot-password",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == 200
    
    def test_forgot_password_missing_email(self, http_client, base_url):
        """Test forgot password without email returns 400."""
        response = http_client.post(
            f"{base_url}/auth/forgot-password",
            json={}
        )
        
        assert response.status_code == 400


class TestAuthLogout:
    """Tests for POST /auth/logout"""
    
    def test_logout_success(self, http_client, base_url, user_token):
        """Test logout returns 204."""
        if not user_token:
            pytest.skip("User token required")
        
        # Get refresh token
        email = pytest.importorskip("os").getenv("TEST_USER_EMAIL")
        password = pytest.importorskip("os").getenv("TEST_USER_PASSWORD")
        
        login_response = http_client.post(
            f"{base_url}/auth/login",
            json={"emailOrUsername": email, "password": password}
        )
        refresh_token = login_response.json().get("refreshToken")
        
        response = http_client.post(
            f"{base_url}/auth/logout",
            json={"refreshToken": refresh_token}
        )
        
        assert response.status_code == 204
    
    def test_logout_without_body(self, http_client, base_url):
        """Test logout without body returns 204."""
        response = http_client.post(f"{base_url}/auth/logout")
        
        assert response.status_code == 204
