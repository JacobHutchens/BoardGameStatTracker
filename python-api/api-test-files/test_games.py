"""
Tests for games endpoints.
"""
import pytest
from conftest import validate_response_shape, make_authenticated_request


@pytest.fixture(scope="function")
def created_game(authenticated_user_client, base_url):
    """Fixture to create a game and return its data. Cleans up after test."""
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    game_data = {
        "gameName": f"Test Game {random_suffix}",
        "description": "Test game description",
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
    
    game = response.json()
    yield game
    
    # Cleanup: delete game if possible (may not be supported, so ignore errors)
    try:
        authenticated_user_client.delete(f"{base_url}/games/{game['id']}")
    except:
        pass


class TestGamesList:
    """Tests for GET /games"""
    
    def test_list_games_success(self, http_client, base_url):
        """Test successful retrieval of games list."""
        response = http_client.get(f"{base_url}/games")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["games", "total", "page"],
            {
                "games": list,
                "total": int,
                "page": int
            }
        )
    
    def test_list_games_with_filter(self, http_client, base_url):
        """Test games list with filter parameter."""
        response = http_client.get(f"{base_url}/games?filter=all")
        
        assert response.status_code == 200
        data = response.json()
        assert "games" in data
    
    def test_list_games_with_search(self, http_client, base_url):
        """Test games list with search parameter."""
        response = http_client.get(f"{base_url}/games?search=test")
        
        assert response.status_code == 200
        data = response.json()
        assert "games" in data
    
    def test_list_games_with_pagination(self, http_client, base_url):
        """Test games list with pagination parameters."""
        response = http_client.get(f"{base_url}/games?page=1&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert "games" in data
        assert "page" in data
        assert data["page"] == 1


class TestGameDetails:
    """Tests for GET /games/{gameId}"""
    
    def test_get_game_details_success(self, http_client, base_url, created_game):
        """Test successful retrieval of game details."""
        game_id = created_game["id"]
        response = http_client.get(f"{base_url}/games/{game_id}")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["id", "gameName", "description", "minPlayerCount", "maxPlayerCount", "canWin", "createdAt"],
            {
                "id": int,
                "gameName": str,
                "description": str,
                "minPlayerCount": int,
                "maxPlayerCount": int,
                "canWin": bool,
                "createdAt": str
            }
        )
        assert data["id"] == game_id
    
    def test_get_game_details_not_found(self, http_client, base_url):
        """Test game details with non-existent ID returns 404."""
        response = http_client.get(f"{base_url}/games/999999")
        
        assert response.status_code == 404
    
    def test_get_game_details_invalid_id(self, http_client, base_url):
        """Test game details with invalid ID format returns 404."""
        response = http_client.get(f"{base_url}/games/invalid")
        
        assert response.status_code == 404


class TestGameCreate:
    """Tests for POST /games"""
    
    def test_create_game_success(self, authenticated_user_client, base_url):
        """Test successful game creation."""
        import random
        import string
        
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        game_data = {
            "gameName": f"New Game {random_suffix}",
            "description": "A new test game",
            "minPlayerCount": 1,
            "maxPlayerCount": 6,
            "canWin": True
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/games",
            json=game_data
        )
        
        assert response.status_code == 201
        data = response.json()
        validate_response_shape(
            response,
            ["id", "gameName", "description", "minPlayerCount", "maxPlayerCount", "canWin", "createdAt"],
            {
                "id": int,
                "gameName": str,
                "minPlayerCount": int,
                "maxPlayerCount": int,
                "canWin": bool
            }
        )
        assert data["gameName"] == game_data["gameName"]
        assert data["minPlayerCount"] == game_data["minPlayerCount"]
        assert data["maxPlayerCount"] == game_data["maxPlayerCount"]
    
    def test_create_game_duplicate_name(self, authenticated_user_client, base_url, created_game):
        """Test creating game with duplicate name returns 409."""
        game_data = {
            "gameName": created_game["gameName"],
            "description": "Duplicate game",
            "minPlayerCount": 2,
            "maxPlayerCount": 4,
            "canWin": True
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/games",
            json=game_data
        )
        
        assert response.status_code == 409
    
    def test_create_game_missing_fields(self, authenticated_user_client, base_url):
        """Test creating game with missing required fields returns 400."""
        response = authenticated_user_client.post(
            f"{base_url}/games",
            json={"gameName": "Incomplete Game"}
        )
        
        assert response.status_code == 400
    
    def test_create_game_invalid_data(self, authenticated_user_client, base_url):
        """Test creating game with invalid data returns 400."""
        game_data = {
            "gameName": "Invalid Game",
            "description": "Test",
            "minPlayerCount": 5,
            "maxPlayerCount": 2,  # max < min
            "canWin": True
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/games",
            json=game_data
        )
        
        assert response.status_code == 400
    
    def test_create_game_unauthorized(self, http_client, base_url):
        """Test creating game without authentication returns 401."""
        game_data = {
            "gameName": "Unauthorized Game",
            "description": "Test",
            "minPlayerCount": 2,
            "maxPlayerCount": 4,
            "canWin": True
        }
        
        response = http_client.post(
            f"{base_url}/games",
            json=game_data
        )
        
        assert response.status_code == 401
