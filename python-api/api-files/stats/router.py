"""
Stats routes: GET /users/me/stats, GET /users/{user_id}/stats, GET /games/{game_id}/stats.
Mounted at /v1 so paths are full: /users/me/stats, /users/{user_id}/stats, /games/{game_id}/stats.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dependencies import get_current_user
from stats.schemas import GameStatsResponse, UserStatsResponse, GameStatsSummary

router = APIRouter()


@router.get("/users/me/stats", response_model=UserStatsResponse)
def get_my_stats(_user=Depends(get_current_user)):
    """Stub: current user full stats (per-game)."""
    return UserStatsResponse(
        games=[
            GameStatsSummary(gameId=1, gameName="Stub Game", played=0, wins=0, winRate=0.0),
        ]
    )


@router.get("/users/{user_id}/stats", response_model=UserStatsResponse)
def get_user_stats(user_id: int):
    """Stub: another user's stats for profile view."""
    return UserStatsResponse(
        games=[
            GameStatsSummary(gameId=1, gameName="Stub Game", played=0, wins=0, winRate=0.0),
        ]
    )


@router.get("/games/{game_id}/stats", response_model=GameStatsResponse)
def get_game_stats(game_id: int, _user=Depends(get_current_user)):
    """Stub: current user's stats for that game."""
    return GameStatsResponse(
        gameId=game_id,
        gameName="Stub Game",
        played=0,
        wins=0,
        winRate=0.0,
    )
