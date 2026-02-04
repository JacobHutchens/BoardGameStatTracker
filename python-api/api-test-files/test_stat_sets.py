"""
Tests for stat sets endpoints (nested under games).
"""
import pytest
from conftest import validate_response_shape


@pytest.fixture(scope="function")
def created_game(authenticated_user_client, base_url):
    """Fixture to create a game for stat set tests."""
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    game_data = {
        "gameName": f"Stat Set Test Game {random_suffix}",
        "description": "Test game for stat sets",
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


@pytest.fixture(scope="function")
def created_stat_set(authenticated_user_client, base_url, created_game):
    """Fixture to create a stat set and return its data."""
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    stat_set_data = {
        "setName": f"Test Stat Set {random_suffix}",
        "stats": [
            {
                "statName": "score",
                "description": "Player score",
                "dataTypeId": 1,  # Assuming integer type exists
                "scopeId": 1  # Assuming player scope exists
            }
        ]
    }
    
    response = authenticated_user_client.post(
        f"{base_url}/games/{created_game['id']}/stat-sets",
        json=stat_set_data
    )
    
    if response.status_code != 201:
        pytest.skip(f"Failed to create stat set: {response.status_code}")
    
    return response.json()


class TestStatSetsList:
    """Tests for GET /games/{gameId}/stat-sets"""
    
    def test_list_stat_sets_success(self, http_client, base_url, created_game):
        """Test successful retrieval of stat sets for a game."""
        game_id = created_game["id"]
        response = http_client.get(f"{base_url}/games/{game_id}/stat-sets")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["statSets"],
            {
                "statSets": list
            }
        )
    
    def test_list_stat_sets_game_not_found(self, http_client, base_url):
        """Test listing stat sets for non-existent game returns 404."""
        response = http_client.get(f"{base_url}/games/999999/stat-sets")
        
        assert response.status_code == 404


class TestStatSetDetails:
    """Tests for GET /games/{gameId}/stat-sets/{statSetId}"""
    
    def test_get_stat_set_details_success(self, http_client, base_url, created_game, created_stat_set):
        """Test successful retrieval of stat set details."""
        game_id = created_game["id"]
        stat_set_id = created_stat_set["id"]
        
        response = http_client.get(f"{base_url}/games/{game_id}/stat-sets/{stat_set_id}")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["id", "gameId", "setName", "userId", "stats"],
            {
                "id": int,
                "gameId": int,
                "setName": str,
                "userId": int,
                "stats": list
            }
        )
        assert data["id"] == stat_set_id
        assert data["gameId"] == game_id
        
        # Validate nested stats structure
        if len(data["stats"]) > 0:
            stat = data["stats"][0]
            assert "statName" in stat
            assert "dataTypeId" in stat
            assert "scopeId" in stat
    
    def test_get_stat_set_details_not_found(self, http_client, base_url, created_game):
        """Test stat set details with non-existent ID returns 404."""
        game_id = created_game["id"]
        response = http_client.get(f"{base_url}/games/{game_id}/stat-sets/999999")
        
        assert response.status_code == 404
    
    def test_get_stat_set_details_wrong_game(self, http_client, base_url, created_game, created_stat_set):
        """Test stat set details with wrong game ID returns 404."""
        stat_set_id = created_stat_set["id"]
        response = http_client.get(f"{base_url}/games/999999/stat-sets/{stat_set_id}")
        
        assert response.status_code == 404


class TestStatSetCreate:
    """Tests for POST /games/{gameId}/stat-sets"""
    
    def test_create_stat_set_success(self, authenticated_user_client, base_url, created_game):
        """Test successful stat set creation."""
        import random
        import string
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        stat_set_data = {
            "setName": f"New Stat Set {random_suffix}",
            "stats": [
                {
                    "statName": "points",
                    "description": "Points scored",
                    "dataTypeId": 1,
                    "scopeId": 1
                },
                {
                    "statName": "rounds",
                    "description": "Rounds played",
                    "dataTypeId": 1,
                    "scopeId": 2
                }
            ]
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/games/{created_game['id']}/stat-sets",
            json=stat_set_data
        )
        
        assert response.status_code == 201
        data = response.json()
        validate_response_shape(
            response,
            ["id", "gameId", "setName", "userId", "stats"],
            {
                "id": int,
                "gameId": int,
                "setName": str,
                "stats": list
            }
        )
        assert data["setName"] == stat_set_data["setName"]
        assert len(data["stats"]) == len(stat_set_data["stats"])
    
    def test_create_stat_set_from_existing(self, authenticated_user_client, base_url, created_game, created_stat_set):
        """Test creating stat set by copying existing one."""
        import random
        import string
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        stat_set_data = {
            "setName": f"Copied Stat Set {random_suffix}",
            "sourceStatSetId": created_stat_set["id"]
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/games/{created_game['id']}/stat-sets",
            json=stat_set_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["setName"] == stat_set_data["setName"]
    
    def test_create_stat_set_game_not_found(self, authenticated_user_client, base_url):
        """Test creating stat set for non-existent game returns 404."""
        stat_set_data = {
            "setName": "Test Stat Set",
            "stats": []
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/games/999999/stat-sets",
            json=stat_set_data
        )
        
        assert response.status_code == 404
    
    def test_create_stat_set_missing_fields(self, authenticated_user_client, base_url, created_game):
        """Test creating stat set with missing fields returns 400."""
        response = authenticated_user_client.post(
            f"{base_url}/games/{created_game['id']}/stat-sets",
            json={}
        )
        
        assert response.status_code == 400
    
    def test_create_stat_set_invalid_data(self, authenticated_user_client, base_url, created_game):
        """Test creating stat set with invalid data returns 422."""
        stat_set_data = {
            "setName": "Invalid Stat Set",
            "stats": [
                {
                    "statName": "invalid",
                    # Missing required fields
                }
            ]
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/games/{created_game['id']}/stat-sets",
            json=stat_set_data
        )
        
        assert response.status_code in [400, 422]
    
    def test_create_stat_set_unauthorized(self, http_client, base_url, created_game):
        """Test creating stat set without authentication returns 401."""
        stat_set_data = {
            "setName": "Unauthorized Stat Set",
            "stats": []
        }
        
        response = http_client.post(
            f"{base_url}/games/{created_game['id']}/stat-sets",
            json=stat_set_data
        )
        
        assert response.status_code == 401
