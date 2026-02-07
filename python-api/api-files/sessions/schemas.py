"""
Pydantic request/response models for sessions.
"""

from pydantic import BaseModel
from typing import Any


class SessionPlayer(BaseModel):
    sessionPlayerId: int
    userId: int | None
    playerName: str
    isSpectator: bool = False
    won: bool | None = None


class SessionCreate(BaseModel):
    gameId: int
    statSetId: int
    invitedUserIds: list[int] = []
    nonAppPlayerNames: list[str] = []


class SessionUpdate(BaseModel):
    timeEnded: str | None = None
    visibilityOverride: str | None = None  # "public" | "private"
    status: str | None = None  # e.g. "ended"


class SessionResponse(BaseModel):
    id: int
    sessionKey: str
    gameId: int
    game: dict[str, Any] | None = None
    statSetId: int
    statSet: dict[str, Any] | None = None
    timeStarted: str
    timeEnded: str | None = None
    currentRound: int | None = None
    visibility: str
    players: list[SessionPlayer]
    trackedStats: list[Any] = []


class SessionCreateResponse(BaseModel):
    sessionId: int
    sessionKey: str


class JoinRequest(BaseModel):
    sessionKey: str


class SessionInviteItem(BaseModel):
    id: int
    sessionId: int
    invitedAt: str
    session: dict[str, Any]


class SessionInviteListResponse(BaseModel):
    invites: list[SessionInviteItem]
    total: int
    page: int


class SessionListResponse(BaseModel):
    sessions: list[SessionResponse]
    total: int
    page: int
