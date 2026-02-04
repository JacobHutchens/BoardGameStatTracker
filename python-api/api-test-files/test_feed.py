"""
Tests for following feed endpoint.
"""
import pytest
from conftest import validate_response_shape


class TestFeed:
    """Tests for GET /feed"""
    
    def test_get_feed_success(self, authenticated_user_client, base_url):
        """Test successful retrieval of following feed."""
        response = authenticated_user_client.get(f"{base_url}/feed")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["sessions", "total", "page"],
            {
                "sessions": list,
                "total": int,
                "page": int
            }
        )
    
    def test_get_feed_with_pagination(self, authenticated_user_client, base_url):
        """Test feed with pagination parameters."""
        response = authenticated_user_client.get(f"{base_url}/feed?page=1&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert data["page"] == 1
    
    def test_get_feed_with_since(self, authenticated_user_client, base_url):
        """Test feed with since parameter."""
        import datetime
        
        # Use a date from the past
        since_date = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
        response = authenticated_user_client.get(f"{base_url}/feed?since={since_date}")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
    
    def test_get_feed_unauthorized(self, http_client, base_url):
        """Test getting feed without authentication returns 401."""
        response = http_client.get(f"{base_url}/feed")
        
        assert response.status_code == 401
