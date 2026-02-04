"""
Tests for social endpoints (followers, following, user search).
"""
import pytest
from conftest import validate_response_shape


@pytest.fixture(scope="function")
def other_user_id(http_client, base_url, authenticated_user_client):
    """Fixture to get another user ID for social tests."""
    # Get current user
    me_response = authenticated_user_client.get(f"{base_url}/users/me")
    if me_response.status_code != 200:
        pytest.skip("Could not get current user")
    
    current_user_id = me_response.json()["id"]
    
    # Try to find another user via search
    search_response = http_client.get(f"{base_url}/users/search?q=test&limit=10")
    if search_response.status_code == 200:
        users = search_response.json().get("users", [])
        for user in users:
            if user.get("id") != current_user_id:
                return user["id"]
    
    # If no other user found, return current user ID (tests may need adjustment)
    return current_user_id


class TestFollowers:
    """Tests for GET /users/{userId}/followers"""
    
    def test_get_followers_success(self, http_client, base_url, other_user_id):
        """Test successful retrieval of followers list."""
        response = http_client.get(f"{base_url}/users/{other_user_id}/followers")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["followers", "total", "page"],
            {
                "followers": list,
                "total": int,
                "page": int
            }
        )
    
    def test_get_followers_with_pagination(self, http_client, base_url, other_user_id):
        """Test followers list with pagination."""
        response = http_client.get(f"{base_url}/users/{other_user_id}/followers?page=1&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert "followers" in data
        assert data["page"] == 1
    
    def test_get_followers_with_search(self, http_client, base_url, other_user_id):
        """Test followers list with search parameter."""
        response = http_client.get(f"{base_url}/users/{other_user_id}/followers?search=test")
        
        assert response.status_code == 200
        data = response.json()
        assert "followers" in data
    
    def test_get_followers_not_found(self, http_client, base_url):
        """Test getting followers for non-existent user returns 404."""
        response = http_client.get(f"{base_url}/users/999999/followers")
        
        assert response.status_code == 404


class TestFollowing:
    """Tests for GET /users/{userId}/following"""
    
    def test_get_following_success(self, http_client, base_url, other_user_id):
        """Test successful retrieval of following list."""
        response = http_client.get(f"{base_url}/users/{other_user_id}/following")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["following", "total", "page"],
            {
                "following": list,
                "total": int,
                "page": int
            }
        )
    
    def test_get_following_with_pagination(self, http_client, base_url, other_user_id):
        """Test following list with pagination."""
        response = http_client.get(f"{base_url}/users/{other_user_id}/following?page=1&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert "following" in data
    
    def test_get_following_not_found(self, http_client, base_url):
        """Test getting following for non-existent user returns 404."""
        response = http_client.get(f"{base_url}/users/999999/following")
        
        assert response.status_code == 404


class TestFollow:
    """Tests for POST /users/{userId}/follow"""
    
    def test_follow_user_success(self, authenticated_user_client, base_url, other_user_id):
        """Test successful follow action."""
        response = authenticated_user_client.post(f"{base_url}/users/{other_user_id}/follow")
        
        assert response.status_code in [200, 204]
        
        # Cleanup: unfollow
        try:
            authenticated_user_client.delete(f"{base_url}/users/{other_user_id}/follow")
        except:
            pass
    
    def test_follow_user_idempotent(self, authenticated_user_client, base_url, other_user_id):
        """Test following same user twice is idempotent."""
        # Follow first time
        response1 = authenticated_user_client.post(f"{base_url}/users/{other_user_id}/follow")
        
        # Follow second time (should be idempotent)
        response2 = authenticated_user_client.post(f"{base_url}/users/{other_user_id}/follow")
        
        assert response1.status_code in [200, 204]
        assert response2.status_code in [200, 204]
        
        # Cleanup
        try:
            authenticated_user_client.delete(f"{base_url}/users/{other_user_id}/follow")
        except:
            pass
    
    def test_follow_user_not_found(self, authenticated_user_client, base_url):
        """Test following non-existent user returns 404."""
        response = authenticated_user_client.post(f"{base_url}/users/999999/follow")
        
        assert response.status_code == 404


class TestUnfollow:
    """Tests for DELETE /users/{userId}/follow"""
    
    def test_unfollow_user_success(self, authenticated_user_client, base_url, other_user_id):
        """Test successful unfollow action."""
        # First follow the user
        authenticated_user_client.post(f"{base_url}/users/{other_user_id}/follow")
        
        # Then unfollow
        response = authenticated_user_client.delete(f"{base_url}/users/{other_user_id}/follow")
        
        assert response.status_code == 204
    
    def test_unfollow_user_not_found(self, authenticated_user_client, base_url):
        """Test unfollowing non-existent user returns 404."""
        response = authenticated_user_client.delete(f"{base_url}/users/999999/follow")
        
        assert response.status_code == 404


class TestUserSearch:
    """Tests for GET /users/search"""
    
    def test_search_users_success(self, http_client, base_url):
        """Test successful user search."""
        response = http_client.get(f"{base_url}/users/search?q=test")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["users", "total", "page"],
            {
                "users": list,
                "total": int,
                "page": int
            }
        )
    
    def test_search_users_with_pagination(self, http_client, base_url):
        """Test user search with pagination."""
        response = http_client.get(f"{base_url}/users/search?q=test&page=1&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert data["page"] == 1
    
    def test_search_users_empty_query(self, http_client, base_url):
        """Test user search with empty query."""
        response = http_client.get(f"{base_url}/users/search?q=")
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
    
    def test_search_users_without_auth(self, http_client, base_url):
        """Test user search works without authentication."""
        response = http_client.get(f"{base_url}/users/search?q=test")
        
        assert response.status_code == 200
