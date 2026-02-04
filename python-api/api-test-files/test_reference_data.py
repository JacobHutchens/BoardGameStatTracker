"""
Tests for reference data endpoints (read-only).
No fixtures needed - these are reference tables.
"""
import pytest
from conftest import validate_response_shape


class TestScopes:
    """Tests for GET /scopes"""
    
    def test_get_scopes_success(self, http_client, base_url):
        """Test successful retrieval of scopes."""
        response = http_client.get(f"{base_url}/scopes")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["scopes"],
            {
                "scopes": [{"id": int, "scope": str}]
            }
        )
        assert isinstance(data["scopes"], list)
        if len(data["scopes"]) > 0:
            assert "id" in data["scopes"][0]
            assert "scope" in data["scopes"][0]
    
    def test_get_scopes_without_auth(self, http_client, base_url):
        """Test scopes endpoint works without authentication."""
        response = http_client.get(f"{base_url}/scopes")
        
        assert response.status_code == 200


class TestDataTypes:
    """Tests for GET /data-types"""
    
    def test_get_data_types_success(self, http_client, base_url):
        """Test successful retrieval of data types."""
        response = http_client.get(f"{base_url}/data-types")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["dataTypes"],
            {
                "dataTypes": [{"id": int, "dataType": str}]
            }
        )
        assert isinstance(data["dataTypes"], list)
        if len(data["dataTypes"]) > 0:
            assert "id" in data["dataTypes"][0]
            assert "dataType" in data["dataTypes"][0]
    
    def test_get_data_types_without_auth(self, http_client, base_url):
        """Test data-types endpoint works without authentication."""
        response = http_client.get(f"{base_url}/data-types")
        
        assert response.status_code == 200
