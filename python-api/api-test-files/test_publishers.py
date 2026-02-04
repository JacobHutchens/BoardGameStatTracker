"""
Tests for publisher endpoints (requires publisher authentication).
"""
import pytest
from conftest import validate_response_shape


class TestPublisherMe:
    """Tests for GET /publishers/me"""
    
    def test_get_publisher_profile_success(self, authenticated_publisher_client, base_url):
        """Test successful retrieval of publisher profile."""
        response = authenticated_publisher_client.get(f"{base_url}/publishers/me")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["id", "name"],
            {
                "id": int,
                "name": str
            }
        )
    
    def test_get_publisher_profile_unauthorized(self, http_client, base_url):
        """Test getting publisher profile without authentication returns 401."""
        response = http_client.get(f"{base_url}/publishers/me")
        
        assert response.status_code == 401
    
    def test_get_publisher_profile_with_user_token(self, authenticated_user_client, base_url):
        """Test getting publisher profile with user token returns 401."""
        response = authenticated_user_client.get(f"{base_url}/publishers/me")
        
        assert response.status_code == 401


class TestPublisherDesigners:
    """Tests for GET /publishers/me/designers"""
    
    def test_get_designers_success(self, authenticated_publisher_client, base_url):
        """Test successful retrieval of designers list."""
        response = authenticated_publisher_client.get(f"{base_url}/publishers/me/designers")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["designers", "total", "page"],
            {
                "designers": list,
                "total": int,
                "page": int
            }
        )
    
    def test_get_designers_with_pagination(self, authenticated_publisher_client, base_url):
        """Test designers list with pagination."""
        response = authenticated_publisher_client.get(
            f"{base_url}/publishers/me/designers?page=1&limit=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "designers" in data
        assert data["page"] == 1
    
    def test_get_designers_unauthorized(self, http_client, base_url):
        """Test getting designers without authentication returns 401."""
        response = http_client.get(f"{base_url}/publishers/me/designers")
        
        assert response.status_code == 401


class TestPublisherDesignerAssign:
    """Tests for POST /publishers/me/designers"""
    
    def test_assign_designer_success(self, authenticated_publisher_client, base_url, authenticated_user_client):
        """Test successful designer tag assignment."""
        # Get a user ID to assign
        user_response = authenticated_user_client.get(f"{base_url}/users/me")
        if user_response.status_code != 200:
            pytest.skip("Could not get user ID")
        
        user_id = user_response.json()["id"]
        
        assign_data = {"userId": user_id}
        response = authenticated_publisher_client.post(
            f"{base_url}/publishers/me/designers",
            json=assign_data
        )
        
        assert response.status_code in [201, 204]
        
        # Cleanup: revoke designer tag
        try:
            authenticated_publisher_client.delete(f"{base_url}/publishers/me/designers/{user_id}")
        except:
            pass
    
    def test_assign_designer_duplicate(self, authenticated_publisher_client, base_url, authenticated_user_client):
        """Test assigning designer tag that's already assigned returns 409."""
        # Get user ID
        user_response = authenticated_user_client.get(f"{base_url}/users/me")
        if user_response.status_code != 200:
            pytest.skip("Could not get user ID")
        
        user_id = user_response.json()["id"]
        
        # Assign first time
        assign_data = {"userId": user_id}
        response1 = authenticated_publisher_client.post(
            f"{base_url}/publishers/me/designers",
            json=assign_data
        )
        
        # Attempt duplicate assignment
        response2 = authenticated_publisher_client.post(
            f"{base_url}/publishers/me/designers",
            json=assign_data
        )
        
        assert response1.status_code in [201, 204]
        assert response2.status_code == 409
        
        # Cleanup
        try:
            authenticated_publisher_client.delete(f"{base_url}/publishers/me/designers/{user_id}")
        except:
            pass
    
    def test_assign_designer_user_not_found(self, authenticated_publisher_client, base_url):
        """Test assigning designer tag to non-existent user returns 404."""
        assign_data = {"userId": 999999}
        response = authenticated_publisher_client.post(
            f"{base_url}/publishers/me/designers",
            json=assign_data
        )
        
        assert response.status_code == 404
    
    def test_assign_designer_missing_user_id(self, authenticated_publisher_client, base_url):
        """Test assigning designer tag without userId returns 400."""
        response = authenticated_publisher_client.post(
            f"{base_url}/publishers/me/designers",
            json={}
        )
        
        assert response.status_code == 400
    
    def test_assign_designer_unauthorized(self, http_client, base_url):
        """Test assigning designer tag without authentication returns 401."""
        response = http_client.post(
            f"{base_url}/publishers/me/designers",
            json={"userId": 1}
        )
        
        assert response.status_code == 401


class TestPublisherDesignerRevoke:
    """Tests for DELETE /publishers/me/designers/{userId}"""
    
    def test_revoke_designer_success(self, authenticated_publisher_client, base_url, authenticated_user_client):
        """Test successful designer tag revocation."""
        # Get user ID
        user_response = authenticated_user_client.get(f"{base_url}/users/me")
        if user_response.status_code != 200:
            pytest.skip("Could not get user ID")
        
        user_id = user_response.json()["id"]
        
        # Assign designer tag first
        authenticated_publisher_client.post(
            f"{base_url}/publishers/me/designers",
            json={"userId": user_id}
        )
        
        # Revoke designer tag
        response = authenticated_publisher_client.delete(
            f"{base_url}/publishers/me/designers/{user_id}"
        )
        
        assert response.status_code == 204
    
    def test_revoke_designer_not_found(self, authenticated_publisher_client, base_url):
        """Test revoking designer tag for non-existent user returns 404."""
        response = authenticated_publisher_client.delete(
            f"{base_url}/publishers/me/designers/999999"
        )
        
        assert response.status_code == 404
    
    def test_revoke_designer_unauthorized(self, http_client, base_url):
        """Test revoking designer tag without authentication returns 401."""
        response = http_client.delete(f"{base_url}/publishers/me/designers/1")
        
        assert response.status_code == 401


class TestPublisherAnalytics:
    """Tests for GET /publishers/me/analytics"""
    
    def test_get_analytics_success(self, authenticated_publisher_client, base_url):
        """Test successful retrieval of publisher analytics."""
        response = authenticated_publisher_client.get(f"{base_url}/publishers/me/analytics")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_analytics_with_date_range(self, authenticated_publisher_client, base_url):
        """Test analytics with date range parameters."""
        response = authenticated_publisher_client.get(
            f"{base_url}/publishers/me/analytics?from=2024-01-01&to=2024-12-31"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_analytics_unauthorized(self, http_client, base_url):
        """Test getting analytics without authentication returns 401."""
        response = http_client.get(f"{base_url}/publishers/me/analytics")
        
        assert response.status_code == 401
