"""
Games routes: GET list, GET by id, POST create. 200 = new game, 211 = game already exists.
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from dependencies import get_current_user_optional, pagination_params
from schemas_common import PaginationParams
from games.schemas import GameCreate, GameResponse, GameListResponse

router = APIRouter()

# Stub in-memory store: name -> game (for duplicate check)
_stub_games: list[dict] = [
    {
        "id": 1,
        "gameName": "Stub Game",
        "description": "A stub game",
        "minPlayerCount": 2,
        "maxPlayerCount": 4,
        "canWin": True,
        "createdAt": "2025-01-01T00:00:00Z",
        "playCount": 0,
        "lastPlayedAt": None,
    }
]
_stub_next_id = 2


# Status 211 = "game already exists" (per Team Lead clarification)
HTTP_GAME_ALREADY_EXISTS = 211


@router.get("", response_model=GameListResponse)
def list_games(
    filter_: str | None = Query(None, alias="filter"),
    search: str | None = None,
    pagination: PaginationParams = Depends(pagination_params),
):
    """Stub: return mock game list with pagination. Filter: my|all|recent."""
    page = pagination.page
    limit = pagination.limit
    start = (page - 1) * limit
    games = _stub_games[start : start + limit]
    return GameListResponse(
        games=[GameResponse(**g) for g in games],
        total=len(_stub_games),
        page=page,
    )


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: int):
    """Stub: return game by id or 404."""
    for g in _stub_games:
        if g["id"] == game_id:
            return GameResponse(**g)
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "not_found", "message": "Game not found"}, "details": []},
    )


@router.post("", response_model=GameResponse, status_code=200)
def create_game(body: GameCreate):
    """Stub: 200 if new game created, 211 if game with same name already exists (with error details)."""
    global _stub_next_id
    for g in _stub_games:
        if g["gameName"] == body.gameName:
            return JSONResponse(
                status_code=HTTP_GAME_ALREADY_EXISTS,
                content={
                    "error": {
                        "code": "game_already_exists",
                        "message": f"A game with the name '{body.gameName}' already exists (id={g['id']}).",
                    },
                    "details": [{"existingGameId": g["id"], "existingGameName": g["gameName"]}],
                },
            )
    new_game = {
        "id": _stub_next_id,
        "gameName": body.gameName,
        "description": body.description,
        "minPlayerCount": body.minPlayerCount,
        "maxPlayerCount": body.maxPlayerCount,
        "canWin": body.canWin,
        "createdAt": "2025-01-01T00:00:00Z",
        "playCount": 0,
        "lastPlayedAt": None,
    }
    _stub_games.append(new_game)
    _stub_next_id += 1
    return GameResponse(**new_game)
