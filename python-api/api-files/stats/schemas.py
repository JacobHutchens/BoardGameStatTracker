"""
Pydantic response models for user stats (per-game, win rate, etc.).
"""

from pydantic import BaseModel
from typing import Any


class GameStatsSummary(BaseModel):
    gameId: int
    gameName: str
    played: int
    wins: int
    winRate: float


class UserStatsResponse(BaseModel):
    """Per-game stats (played, wins, win rate)."""

    games: list[GameStatsSummary] = []


class GameStatsResponse(BaseModel):
    """Current user's stats for one game."""

    gameId: int
    gameName: str
    played: int
    wins: int
    winRate: float
