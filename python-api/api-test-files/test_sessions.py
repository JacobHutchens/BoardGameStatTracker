"""
Tests for sessions endpoints.
"""
import pytest
from conftest import validate_response_shape


@pytest.fixture(scope="function")
def created_game(authenticated_user_client, base_url):
    """Fixture to create a game for session tests."""
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    game_data = {
        "gameName": f"Session Test Game {random_suffix}",
        "description": "Test game for sessions",
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
    """Fixture to create a stat set for session tests."""
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    stat_set_data = {
        "setName": f"Session Test Stat Set {random_suffix}",
        "stats": [
            {
                "statName": "score",
                "description": "Player score",
                "dataTypeId": 1,
                "scopeId": 1
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


@pytest.fixture(scope="function")
def created_session(authenticated_user_client, base_url, created_game, created_stat_set):
    """Fixture to create a session and return its data. Cleans up after test."""
    session_data = {
        "gameId": created_game["id"],
        "statSetId": created_stat_set["id"],
        "invitedUserIds": [],
        "nonAppPlayerNames": []
    }
    
    response = authenticated_user_client.post(
        f"{base_url}/sessions",
        json=session_data
    )
    
    if response.status_code != 201:
        pytest.skip(f"Failed to create session: {response.status_code}")
    
    session = response.json()
    yield session
    
    # Cleanup: delete session
    try:
        authenticated_user_client.delete(f"{base_url}/sessions/{session['sessionId']}")
    except:
        pass


class TestSessionsList:
    """Tests for GET /sessions"""
    
    def test_list_sessions_success(self, authenticated_user_client, base_url):
        """Test successful retrieval of sessions list."""
        response = authenticated_user_client.get(f"{base_url}/sessions")
        
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
    
    def test_list_sessions_active_filter(self, authenticated_user_client, base_url):
        """Test sessions list with active filter."""
        response = authenticated_user_client.get(f"{base_url}/sessions?active=true")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
    
    def test_list_sessions_history_filter(self, authenticated_user_client, base_url):
        """Test sessions list with history filter."""
        response = authenticated_user_client.get(f"{base_url}/sessions?active=false")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
    
    def test_list_sessions_with_game_filter(self, authenticated_user_client, base_url, created_game):
        """Test sessions list filtered by game."""
        response = authenticated_user_client.get(f"{base_url}/sessions?gameId={created_game['id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
    
    def test_list_sessions_with_pagination(self, authenticated_user_client, base_url):
        """Test sessions list with pagination."""
        response = authenticated_user_client.get(f"{base_url}/sessions?page=1&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert data["page"] == 1


class TestSessionDetails:
    """Tests for GET /sessions/{sessionId}"""
    
    def test_get_session_details_success(self, authenticated_user_client, base_url, created_session):
        """Test successful retrieval of session details."""
        session_id = created_session["sessionId"]
        response = authenticated_user_client.get(f"{base_url}/sessions/{session_id}")
        
        assert response.status_code == 200
        data = response.json()
        validate_response_shape(
            response,
            ["id", "sessionKey", "gameId", "game", "statSetId", "statSet", "timeStarted", "visibility", "players"],
            {
                "id": int,
                "sessionKey": str,
                "gameId": int,
                "statSetId": int,
                "visibility": str,
                "players": list
            }
        )
        assert data["id"] == session_id
    
    def test_get_session_details_not_found(self, authenticated_user_client, base_url):
        """Test session details with non-existent ID returns 404."""
        response = authenticated_user_client.get(f"{base_url}/sessions/999999")
        
        assert response.status_code == 404
    
    def test_get_session_details_forbidden(self, authenticated_user_client, http_client, base_url, created_session):
        """Test session details for session user doesn't have access to returns 403."""
        # Use unauthenticated client or different user
        session_id = created_session["sessionId"]
        response = http_client.get(f"{base_url}/sessions/{session_id}")
        
        # May return 401 or 403 depending on implementation
        assert response.status_code in [401, 403]


class TestSessionCreate:
    """Tests for POST /sessions"""
    
    def test_create_session_success(self, authenticated_user_client, base_url, created_game, created_stat_set):
        """Test successful session creation."""
        session_data = {
            "gameId": created_game["id"],
            "statSetId": created_stat_set["id"],
            "invitedUserIds": [],
            "nonAppPlayerNames": ["Player 1", "Player 2"]
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/sessions",
            json=session_data
        )
        
        assert response.status_code == 201
        data = response.json()
        validate_response_shape(
            response,
            ["sessionId", "sessionKey"],
            {
                "sessionId": int,
                "sessionKey": str
            }
        )
        
        # Cleanup
        try:
            authenticated_user_client.delete(f"{base_url}/sessions/{data['sessionId']}")
        except:
            pass
    
    def test_create_session_game_not_found(self, authenticated_user_client, base_url, created_stat_set):
        """Test creating session with non-existent game returns 404."""
        session_data = {
            "gameId": 999999,
            "statSetId": created_stat_set["id"],
            "invitedUserIds": [],
            "nonAppPlayerNames": []
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/sessions",
            json=session_data
        )
        
        assert response.status_code == 404
    
    def test_create_session_stat_set_not_found(self, authenticated_user_client, base_url, created_game):
        """Test creating session with non-existent stat set returns 404."""
        session_data = {
            "gameId": created_game["id"],
            "statSetId": 999999,
            "invitedUserIds": [],
            "nonAppPlayerNames": []
        }
        
        response = authenticated_user_client.post(
            f"{base_url}/sessions",
            json=session_data
        )
        
        assert response.status_code == 404
    
    def test_create_session_missing_fields(self, authenticated_user_client, base_url):
        """Test creating session with missing fields returns 400 or 422."""
        response = authenticated_user_client.post(
            f"{base_url}/sessions",
            json={}
        )
        
        assert response.status_code in [400, 422]
    
    def test_create_session_unauthorized(self, http_client, base_url, created_game, created_stat_set):
        """Test creating session without authentication returns 401."""
        session_data = {
            "gameId": created_game["id"],
            "statSetId": created_stat_set["id"],
            "invitedUserIds": [],
            "nonAppPlayerNames": []
        }
        
        response = http_client.post(
            f"{base_url}/sessions",
            json=session_data
        )
        
        assert response.status_code == 401


class TestSessionUpdate:
    """Tests for PATCH /sessions/{sessionId}"""
    
    def test_update_session_success(self, authenticated_user_client, base_url, created_session):
        """Test successful session update."""
        session_id = created_session["sessionId"]
        update_data = {
            "status": "ended"
        }
        
        response = authenticated_user_client.patch(
            f"{base_url}/sessions/{session_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
    
    def test_update_session_not_found(self, authenticated_user_client, base_url):
        """Test updating non-existent session returns 404."""
        response = authenticated_user_client.patch(
            f"{base_url}/sessions/999999",
            json={"status": "ended"}
        )
        
        assert response.status_code == 404
    
    def test_update_session_forbidden(self, authenticated_user_client, http_client, base_url, created_session):
        """Test updating session user doesn't own returns 403."""
        session_id = created_session["sessionId"]
        response = http_client.patch(
            f"{base_url}/sessions/{session_id}",
            json={"status": "ended"}
        )
        
        assert response.status_code in [401, 403]


class TestSessionDelete:
    """Tests for DELETE /sessions/{sessionId}"""
    
    def test_delete_session_success(self, authenticated_user_client, base_url, created_game, created_stat_set):
        """Test successful session deletion."""
        # Create session first
        session_data = {
            "gameId": created_game["id"],
            "statSetId": created_stat_set["id"],
            "invitedUserIds": [],
            "nonAppPlayerNames": []
        }
        
        create_response = authenticated_user_client.post(
            f"{base_url}/sessions",
            json=session_data
        )
        
        if create_response.status_code != 201:
            pytest.skip("Failed to create session for delete test")
        
        session_id = create_response.json()["sessionId"]
        
        # Delete session
        response = authenticated_user_client.delete(f"{base_url}/sessions/{session_id}")
        
        assert response.status_code == 204
    
    def test_delete_session_not_found(self, authenticated_user_client, base_url):
        """Test deleting non-existent session returns 404."""
        response = authenticated_user_client.delete(f"{base_url}/sessions/999999")
        
        assert response.status_code == 404


class TestSessionJoin:
    """Tests for POST /sessions/join"""
    
    def test_join_session_success(self, authenticated_user_client, base_url, created_session):
        """Test successful session join."""
        session_key = created_session["sessionKey"]
        
        response = authenticated_user_client.post(
            f"{base_url}/sessions/join",
            json={"sessionKey": session_key}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["sessionKey"] == session_key
    
    def test_join_session_idempotent(self, authenticated_user_client, base_url, created_session):
        """Test joining already-joined session returns 200 (idempotent)."""
        session_key = created_session["sessionKey"]
        
        # Join first time
        response1 = authenticated_user_client.post(
            f"{base_url}/sessions/join",
            json={"sessionKey": session_key}
        )
        
        # Join second time (should be idempotent)
        response2 = authenticated_user_client.post(
            f"{base_url}/sessions/join",
            json={"sessionKey": session_key}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
    
    def test_join_session_not_found(self, authenticated_user_client, base_url):
        """Test joining non-existent session returns 404."""
        response = authenticated_user_client.post(
            f"{base_url}/sessions/join",
            json={"sessionKey": "invalid_key_12345"}
        )
        
        assert response.status_code == 404
    
    def test_join_session_missing_key(self, authenticated_user_client, base_url):
        """Test joining session without key returns 400."""
        response = authenticated_user_client.post(
            f"{base_url}/sessions/join",
            json={}
        )
        
        assert response.status_code == 400
