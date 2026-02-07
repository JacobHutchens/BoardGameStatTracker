"""
Pydantic request/response models for games.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class GameCreate(BaseModel):
    gameName: str
    description: str = ""
    minPlayerCount: int = 1
    maxPlayerCount: int = 99
    canWin: bool = True


class GameResponse(BaseModel):
    id: int
    gameName: str
    description: str
    minPlayerCount: int
    maxPlayerCount: int
    canWin: bool
    createdAt: str
    playCount: int | None = None
    lastPlayedAt: str | None = None


class GameListResponse(BaseModel):
    games: list[GameResponse]
    total: int
    page: int
