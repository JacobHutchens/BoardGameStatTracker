"""
Sessions routes: list, get, create, PATCH, DELETE, join, invites. Mounted at /v1/sessions.
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, Response

from dependencies import get_current_user, pagination_params
from schemas_common import PaginationParams
from sessions.schemas import (
    SessionCreate,
    SessionCreateResponse,
    SessionInviteItem,
    SessionInviteListResponse,
    SessionListResponse,
    SessionPlayer,
    SessionResponse,
    SessionUpdate,
    JoinRequest,
)

router = APIRouter()

_stub_sessions: list[dict] = [
    {
        "id": 1,
        "sessionKey": "STUB-KEY-1",
        "gameId": 1,
        "game": {"id": 1, "gameName": "Stub Game"},
        "statSetId": 1,
        "statSet": {"id": 1, "setName": "Default Set"},
        "timeStarted": "2025-01-01T12:00:00Z",
        "timeEnded": None,
        "currentRound": 1,
        "visibility": "public",
        "players": [
            {"sessionPlayerId": 1, "userId": 1, "playerName": "stub_user", "isSpectator": False, "won": None},
        ],
        "trackedStats": [],
    }
]
_stub_invites: list[dict] = []
_stub_next_id = 2


@router.get("", response_model=SessionListResponse)
def list_sessions(
    active: bool | None = Query(None),
    from_: str | None = Query(None, alias="from"),
    to: str | None = None,
    gameId: int | None = None,
    pagination: PaginationParams = Depends(pagination_params),
    _user=Depends(get_current_user),
):
    """Stub: list sessions (active or history) with pagination."""
    page = pagination.page
    limit = pagination.limit
    start = (page - 1) * limit
    items = _stub_sessions[start : start + limit]
    return SessionListResponse(
        sessions=[SessionResponse(**s) for s in items],
        total=len(_stub_sessions),
        page=page,
    )


@router.get("/invites", response_model=SessionInviteListResponse)
def list_invites(
    pending: bool | None = Query(True),
    pagination: PaginationParams = Depends(pagination_params),
    _user=Depends(get_current_user),
):
    """Stub: list session invites for current user."""
    page = pagination.page
    limit = pagination.limit
    start = (page - 1) * limit
    items = _stub_invites[start : start + limit]
    return SessionInviteListResponse(
        invites=[SessionInviteItem(**i) for i in items],
        total=len(_stub_invites),
        page=page,
    )


@router.post("/join", response_model=SessionResponse, status_code=200)
def join_session(body: JoinRequest, _user=Depends(get_current_user)):
    """Stub: join by session key (idempotent). 404 not found, 409 full/ended."""
    for s in _stub_sessions:
        if s["sessionKey"] == body.sessionKey:
            return SessionResponse(**s)
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "not_found", "message": "Session not found"}, "details": []},
    )


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, _user=Depends(get_current_user)):
    """Stub: session details or 403/404."""
    for s in _stub_sessions:
        if s["id"] == session_id:
            return SessionResponse(**s)
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "not_found", "message": "Session not found"}, "details": []},
    )


@router.post("", response_model=SessionCreateResponse, status_code=201)
def create_session(body: SessionCreate, _user=Depends(get_current_user)):
    """Stub: create session; 403 if at weekly limit (designers exempt)."""
    global _stub_next_id
    new_id = _stub_next_id
    _stub_next_id += 1
    key = f"STUB-KEY-{new_id}"
    new_sess = {
        "id": new_id,
        "sessionKey": key,
        "gameId": body.gameId,
        "game": {"id": body.gameId, "gameName": "Stub Game"},
        "statSetId": body.statSetId,
        "statSet": {"id": body.statSetId, "setName": "Default"},
        "timeStarted": "2025-01-01T12:00:00Z",
        "timeEnded": None,
        "currentRound": 1,
        "visibility": "public",
        "players": [{"sessionPlayerId": 1, "userId": _user["id"], "playerName": _user["username"], "isSpectator": False, "won": None}],
        "trackedStats": [],
    }
    _stub_sessions.append(new_sess)
    return SessionCreateResponse(sessionId=new_id, sessionKey=key)


@router.patch("/{session_id}", response_model=SessionResponse)
def update_session(session_id: int, body: SessionUpdate, _user=Depends(get_current_user)):
    """Stub: end session or update visibility."""
    for s in _stub_sessions:
        if s["id"] == session_id:
            if body.timeEnded is not None:
                s["timeEnded"] = body.timeEnded
            if body.visibilityOverride is not None:
                s["visibility"] = body.visibilityOverride
            if body.status == "ended" and s["timeEnded"] is None:
                s["timeEnded"] = "2025-01-01T14:00:00Z"
            return SessionResponse(**s)
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "not_found", "message": "Session not found"}, "details": []},
    )


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: int, _user=Depends(get_current_user)):
    """Stub: delete session or 403/404."""
    global _stub_sessions
    for i, s in enumerate(_stub_sessions):
        if s["id"] == session_id:
            _stub_sessions.pop(i)
            return Response(status_code=204)
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "not_found", "message": "Session not found"}, "details": []},
    )
