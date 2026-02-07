"""
Stat sets routes: GET list, GET by id, POST create. Mounted at /v1/games/{game_id}/stat-sets.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dependencies import get_current_user_optional
from stat_sets.schemas import (
    StatSetCreate,
    StatSetCreateStat,
    StatSetListItem,
    StatSetListResponse,
    StatSetResponse,
    StatDefinition,
)

router = APIRouter()

# Stub store per game_id
_stub_stat_sets: list[dict] = [
    {
        "id": 1,
        "gameId": 1,
        "setName": "Default Set",
        "userId": 1,
        "stats": [
            {"id": 1, "statName": "player_won", "description": "Player won", "dataTypeId": 3, "scopeId": 1},
        ],
    }
]
_stub_next_id = 2


@router.get("", response_model=StatSetListResponse)
def list_stat_sets(game_id: int):
    """Stub: return stat sets for the game (404 if game unknown)."""
    sets = [s for s in _stub_stat_sets if s["gameId"] == game_id]
    return StatSetListResponse(
        statSets=[
            StatSetListItem(
                id=s["id"],
                setName=s["setName"],
                stats=[{"statName": st["statName"], "dataTypeId": st["dataTypeId"], "scopeId": st["scopeId"]} for st in s["stats"]],
            )
            for s in sets
        ]
    )


@router.get("/{stat_set_id}", response_model=StatSetResponse)
def get_stat_set(game_id: int, stat_set_id: int):
    """Stub: return one stat set or 404."""
    for s in _stub_stat_sets:
        if s["gameId"] == game_id and s["id"] == stat_set_id:
            return StatSetResponse(
                id=s["id"],
                gameId=s["gameId"],
                setName=s["setName"],
                userId=s["userId"],
                stats=[StatDefinition(**st) for st in s["stats"]],
            )
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "not_found", "message": "Stat set not found"}, "details": []},
    )


@router.post("", response_model=StatSetResponse, status_code=201)
def create_stat_set(game_id: int, body: StatSetCreate):
    """Stub: create stat set (optionally copy from sourceStatSetId)."""
    global _stub_next_id
    stats = []
    if body.sourceStatSetId is not None:
        for s in _stub_stat_sets:
            if s["id"] == body.sourceStatSetId and s["gameId"] == game_id:
                stats = [{**st, "id": _stub_next_id + i} for i, st in enumerate(s["stats"])]
                break
    elif body.stats:
        stats = [
            {"id": _stub_next_id + i, "statName": st.statName, "description": st.description, "dataTypeId": st.dataTypeId, "scopeId": st.scopeId}
            for i, st in enumerate(body.stats)
        ]
    new_id = _stub_next_id
    _stub_next_id += 1
    new_set = {
        "id": new_id,
        "gameId": game_id,
        "setName": body.setName,
        "userId": 1,
        "stats": stats if stats else [{"id": new_id, "statName": "score", "description": "", "dataTypeId": 1, "scopeId": 1}],
    }
    _stub_stat_sets.append(new_set)
    return StatSetResponse(
        id=new_set["id"],
        gameId=new_set["gameId"],
        setName=new_set["setName"],
        userId=new_set["userId"],
        stats=[StatDefinition(**st) for st in new_set["stats"]],
    )
