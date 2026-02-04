"""
Tests for user stats endpoints.
"""
import pytest
from conftest import validate_response_shape


@pytest.fixture(scope="function")
def created_game(authenticated_user_client, base_url):
    """Fixture to create a game for stats tests."""
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    game_data = {
        "gameName": f"Stats Test Game {random_suffix}",
        "description": "Test game for stats",
        "minPlayerCount": 2,
        "maxPlayerCount": 4,
        "canWin": True
    }
    
    response = authenticated_user_client.post(
        f"{base_url}/games",
        json=game_data
    )
    
    if response.status_code != 201:
        pytest.skip(f"Failed to create game: {response.status_code}")
    
    return response.json()


class TestUserStatsMe:
    """Tests for GET /users/me/stats"""
    
    def test_get_user_stats_success(self, authenticated_user_client, base_url):
        """Test successful retrieval of current user's stats."""
        response = authenticated_user_client.get(f"{base_url}/users/me/stats")
        
        assert response.status_code == 200
        data = response.json()
        # Response shape may vary, but should be valid JSON
        assert isinstance(data, dict)
    
    def test_get_user_stats_unauthorized(self, http_client, base_url):
        """Test getting user stats without authentication returns 401."""
        response = http_client.get(f"{base_url}/users/me/stats")
        
        assert response.status_code == 401


class TestUserStatsOther:
    """Tests for GET /users/{userId}/stats"""
    
    def test_get_other_user_stats_success(self, http_client, base_url, authenticated_user_client):
        """Test successful retrieval of another user's stats."""
        # Get current user ID
        me_response = authenticated_user_client.get(f"{base_url}/users/me")
        if me_response.status_code != 200:
            pytest.skip("Could not get current user")
        
        user_id = me_response.json()["id"]
        
        response = http_client.get(f"{base_url}/users/{user_id}/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_other_user_stats_not_found(self, http_client, base_url):
        """Test getting stats for non-existent user returns 404."""
        response = http_client.get(f"{base_url}/users/999999/stats")
        
        assert response.status_code == 404


class TestGameStats:
    """Tests for GET /games/{gameId}/stats"""
    
    def test_get_game_stats_success(self, authenticated_user_client, base_url, created_game):
        """Test successful retrieval of current user's stats for a game."""
        game_id = created_game["id"]
        response = authenticated_user_client.get(f"{base_url}/games/{game_id}/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_game_stats_not_found(self, authenticated_user_client, base_url):
        """Test getting stats for non-existent game returns 404."""
        response = authenticated_user_client.get(f"{base_url}/games/999999/stats")
        
        assert response.status_code == 404
    
    def test_get_game_stats_unauthorized(self, http_client, base_url, created_game):
        """Test getting game stats without authentication returns 401."""
        game_id = created_game["id"]
        response = http_client.get(f"{base_url}/games/{game_id}/stats")
        
        assert response.status_code == 401
