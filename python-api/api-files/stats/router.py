"""
Stats routes: GET /users/me/stats, GET /users/{user_id}/stats, GET /games/{game_id}/stats.
Mounted at /v1. DB-backed from user_game_stats_cache; win rate = wins/played when played > 0.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import User, Game, UserGameStatsCache
from dependencies import get_current_user
from stats.schemas import GameStatsResponse, UserStatsResponse, GameStatsSummary

router = APIRouter()


def _error_body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}, "details": []}


def _win_rate(played: int, wins: int | None) -> float:
    if played <= 0:
        return 0.0
    return (wins or 0) / played


@router.get("/users/me/stats", response_model=UserStatsResponse)
async def get_my_stats(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Current user full stats (per-game from user_game_stats_cache)."""
    user_id = current_user["id"]
    stmt = (
        select(UserGameStatsCache, Game)
        .join(Game, UserGameStatsCache.game_id == Game.id)
        .where(UserGameStatsCache.user_id == user_id)
    )
    result = await session.execute(stmt)
    rows = result.all()
    games = [
        GameStatsSummary(
            gameId=row[0].game_id,
            gameName=row[1].game_name,
            played=row[0].total_times_played,
            wins=row[0].wins or 0,
            winRate=_win_rate(row[0].total_times_played, row[0].wins),
        )
        for row in rows
    ]
    return UserStatsResponse(games=games)


@router.get("/users/{user_id}/stats", response_model=UserStatsResponse)
async def get_user_stats(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Another user's stats for profile view. 404 if user not found."""
    user = await session.get(User, user_id)
    if not user:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "User not found"),
        )
    stmt = (
        select(UserGameStatsCache, Game)
        .join(Game, UserGameStatsCache.game_id == Game.id)
        .where(UserGameStatsCache.user_id == user_id)
    )
    result = await session.execute(stmt)
    rows = result.all()
    games = [
        GameStatsSummary(
            gameId=row[0].game_id,
            gameName=row[1].game_name,
            played=row[0].total_times_played,
            wins=row[0].wins or 0,
            winRate=_win_rate(row[0].total_times_played, row[0].wins),
        )
        for row in rows
    ]
    return UserStatsResponse(games=games)


@router.get("/games/{game_id}/stats", response_model=GameStatsResponse)
async def get_game_stats(
    game_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Current user's stats for that game. 404 if game not found."""
    game = await session.get(Game, game_id)
    if not game:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Game not found"),
        )
    stmt = select(UserGameStatsCache).where(
        UserGameStatsCache.user_id == current_user["id"],
        UserGameStatsCache.game_id == game_id,
    )
    result = await session.execute(stmt)
    row = result.scalars().first()
    if not row:
        return GameStatsResponse(
            gameId=game_id,
            gameName=game.game_name,
            played=0,
            wins=0,
            winRate=0.0,
        )
    return GameStatsResponse(
        gameId=game_id,
        gameName=game.game_name,
        played=row.total_times_played,
        wins=row.wins or 0,
        winRate=_win_rate(row.total_times_played, row.wins),
    )
