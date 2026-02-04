"""
Tests for export endpoints.
"""
import pytest
from conftest import validate_response_shape


class TestExportGet:
    """Tests for GET /users/me/export"""
    
    def test_export_preview_success(self, authenticated_user_client, base_url):
        """Test successful export preview."""
        response = authenticated_user_client.get(f"{base_url}/users/me/export?preview=true")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["sessionCount", "statValueCount", "estimatedSizeBytes"],
            {
                "sessionCount": int,
                "statValueCount": int,
                "estimatedSizeBytes": int
            }
        )
    
    def test_export_preview_with_filters(self, authenticated_user_client, base_url):
        """Test export preview with filter parameters."""
        response = authenticated_user_client.get(
            f"{base_url}/users/me/export?preview=true&gameIds=1,2&from=2024-01-01&to=2024-12-31"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "sessionCount" in data
    
    def test_export_without_preview(self, authenticated_user_client, base_url):
        """Test export without preview returns export data."""
        response = authenticated_user_client.get(f"{base_url}/users/me/export")
        
        assert response.status_code == 200
        # May return JSON or stream depending on implementation
        assert response.headers.get("Content-Type") is not None
    
    def test_export_invalid_date_range(self, authenticated_user_client, base_url):
        """Test export with invalid date range returns 422."""
        response = authenticated_user_client.get(
            f"{base_url}/users/me/export?preview=true&from=2024-12-31&to=2024-01-01"  # Invalid: to < from
        )
        
        assert response.status_code == 422
    
    def test_export_unauthorized(self, http_client, base_url):
        """Test export without authentication returns 401."""
        response = http_client.get(f"{base_url}/users/me/export?preview=true")
        
        assert response.status_code == 401


class TestExportPost:
    """Tests for POST /users/me/export"""
    
    def test_export_post_preview_success(self, authenticated_user_client, base_url):
        """Test successful export preview via POST."""
        export_data = {
            "preview": True
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/users/me/export",
            json=export_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "sessionCount" in data
    
    def test_export_post_with_filters(self, authenticated_user_client, base_url):
        """Test export POST with complex filters."""
        export_data = {
            "gameIds": [1, 2],
            "from": "2024-01-01",
            "to": "2024-12-31",
            "preview": True
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/users/me/export",
            json=export_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "sessionCount" in data
    
    def test_export_post_invalid_filters(self, authenticated_user_client, base_url):
        """Test export POST with invalid filters returns 422."""
        export_data = {
            "from": "2024-12-31",
            "to": "2024-01-01",  # Invalid: to < from
            "preview": True
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/users/me/export",
            json=export_data
        )
        
        assert response.status_code == 422
    
    def test_export_post_unauthorized(self, http_client, base_url):
        """Test export POST without authentication returns 401."""
        response = http_client.post(
            f"{base_url}/users/me/export",
            json={"preview": True}
        )
        
        assert response.status_code == 401
