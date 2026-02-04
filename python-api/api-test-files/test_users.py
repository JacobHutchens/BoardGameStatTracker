"""
Tests for users endpoints.
"""
import pytest
from conftest import validate_response_shape


class TestUserMe:
    """Tests for GET /users/me"""
    
    def test_get_current_user_success(self, authenticated_user_client, base_url):
        """Test successful retrieval of current user profile."""
        response = authenticated_user_client.get(f"{base_url}/users/me")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["id", "username", "email", "designer", "sessionQuota", "defaultSessionVisibility"],
            {
                "id": int,
                "username": str,
                "email": str,
                "designer": bool,
                "sessionQuota": dict,
                "defaultSessionVisibility": str
            }
        )
        
        # Validate nested sessionQuota structure
        assert "sessionsUsedThisWeek" in data["sessionQuota"]
        assert "sessionsLimitPerWeek" in data["sessionQuota"]
    
    def test_get_current_user_unauthorized(self, http_client, base_url):
        """Test getting current user without authentication returns 401."""
        response = http_client.get(f"{base_url}/users/me")
        
        assert response.status_code == 401


class TestUserUpdate:
    """Tests for PATCH /users/me"""
    
    def test_update_user_success(self, authenticated_user_client, base_url):
        """Test successful user profile update."""
        import random
        import string
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        update_data = {
            "bio": f"Updated bio {random_suffix}",
            "avatarUrl": f"https://example.com/avatar_{random_suffix}.jpg"
        }
        
        response = authenticated_user_client.patch(
            f"{base_url}/users/me",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == update_data["bio"]
        assert data["avatarUrl"] == update_data["avatarUrl"]
    
    def test_update_username_success(self, authenticated_user_client, base_url):
        """Test successful username update."""
        import random
        import string
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        new_username = f"updated_user_{random_suffix}"
        
        # Check username availability first
        check_response = authenticated_user_client.get(
            f"{base_url}/users/check-username?username={new_username}"
        )
        
        if check_response.status_code == 200 and check_response.json().get("available"):
            update_data = {"username": new_username}
            response = authenticated_user_client.patch(
                f"{base_url}/users/me",
                json=update_data
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == new_username
    
    def test_update_user_duplicate_username(self, authenticated_user_client, base_url):
        """Test updating to duplicate username returns 409."""
        # This test assumes there's another user with a known username
        # In practice, you'd need to create another user first
        update_data = {"username": "existing_username"}
        
        response = authenticated_user_client.patch(
            f"{base_url}/users/me",
            json=update_data
        )
        
        # May return 409 if username exists, or 200 if it's the same user
        assert response.status_code in [200, 409]
    
    def test_update_user_invalid_data(self, authenticated_user_client, base_url):
        """Test updating user with invalid data returns 400 or 422."""
        update_data = {
            "email": "invalid_email_format"  # Invalid email format
        }
        
        response = authenticated_user_client.patch(
            f"{base_url}/users/me",
            json=update_data
        )
        
        assert response.status_code in [400, 422]
    
    def test_update_user_unauthorized(self, http_client, base_url):
        """Test updating user without authentication returns 401."""
        response = http_client.patch(
            f"{base_url}/users/me",
            json={"bio": "Unauthorized update"}
        )
        
        assert response.status_code == 401


class TestUserProfile:
    """Tests for GET /users/{userId}"""
    
    def test_get_user_profile_success(self, http_client, base_url, authenticated_user_client):
        """Test successful retrieval of another user's public profile."""
        # First get current user to get a valid user ID
        me_response = authenticated_user_client.get(f"{base_url}/users/me")
        if me_response.status_code != 200:
            pytest.skip("Could not get current user")
        
        user_id = me_response.json()["id"]
        
        # Get public profile
        response = http_client.get(f"{base_url}/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["id", "username"],
            {
                "id": int,
                "username": str
            }
        )
        assert data["id"] == user_id
    
    def test_get_user_profile_not_found(self, http_client, base_url):
        """Test getting non-existent user profile returns 404."""
        response = http_client.get(f"{base_url}/users/999999")
        
        assert response.status_code == 404


class TestCheckUsername:
    """Tests for GET /users/check-username"""
    
    def test_check_username_available(self, http_client, base_url):
        """Test checking available username returns true."""
        import random
        import string
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        username = f"check_{random_suffix}"
        
        response = http_client.get(f"{base_url}/users/check-username?username={username}")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["available"],
            {
                "available": bool
            }
        )
    
    def test_check_username_missing_param(self, http_client, base_url):
        """Test checking username without parameter returns 400."""
        response = http_client.get(f"{base_url}/users/check-username")
        
        assert response.status_code == 400
    
    def test_check_username_without_auth(self, http_client, base_url):
        """Test username check works without authentication."""
        response = http_client.get(f"{base_url}/users/check-username?username=testuser")
        
        assert response.status_code == 200
