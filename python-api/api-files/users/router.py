"""
Users routes: GET/PATCH /me, GET /{user_id}, GET /check-username. Mounted at /v1/users.
All handlers are DB-backed; session quota uses week (Sunday–Saturday) in user timezone.
"""

import os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import User, Session, UserGameStatsCache, Game
from dependencies import get_current_user
from users.schemas import (
    CheckUsernameResponse,
    UserMeResponse,
    UserMeUpdate,
    UserPublicResponse,
    SessionQuota,
)

router = APIRouter()

# Session limit: default 2 per week; designers exempt (limit null).
DEFAULT_SESSION_LIMIT = 2
USER_TZ_DEFAULT = "America/Los_Angeles"  # UTC-8 when user.time_zone is null


def _get_session_limit_per_week() -> int:
    raw = os.getenv("SESSION_LIMIT_PER_WEEK")
    if raw is None or raw == "":
        return DEFAULT_SESSION_LIMIT
    try:
        return max(1, int(raw))
    except ValueError:
        return DEFAULT_SESSION_LIMIT


def _week_bounds_utc(tz_name: str) -> tuple[datetime, datetime]:
    """
    Current week in the given IANA timezone: Sunday 00:00:00.000 to Saturday 23:59:59.999.
    Returns (week_start, week_end) as timezone-aware UTC datetimes.
    """
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    # Python: Monday=0, Sunday=6 → days since Sunday = (weekday() + 1) % 7
    days_since_sunday = (now.weekday() + 1) % 7
    week_start = (now - timedelta(days=days_since_sunday)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    week_end = week_start + timedelta(
        days=6, hours=23, minutes=59, seconds=59, microseconds=999999
    )
    return week_start.astimezone(timezone.utc), week_end.astimezone(timezone.utc)


async def _sessions_used_this_week(
    session: AsyncSession, user_id: int, tz_name: str
) -> int:
    """Count sessions created by user in the current week (Sunday–Saturday) in that timezone."""
    week_start, week_end = _week_bounds_utc(tz_name)
    stmt = select(func.count(Session.id)).where(
        Session.creator_user_id == user_id,
        Session.time_started >= week_start,
        Session.time_started <= week_end,
    )
    result = await session.execute(stmt)
    return result.scalar() or 0


def _error_body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}, "details": []}


async def _compute_quick_stats(
    session: AsyncSession, user_id: int, tz_name: str
) -> dict | None:
    """Build quickStats from UserGameStatsCache and sessionsThisWeek. Returns None if no stats."""
    stmt = (
        select(UserGameStatsCache, Game)
        .join(Game, UserGameStatsCache.game_id == Game.id)
        .where(UserGameStatsCache.user_id == user_id)
    )
    result = await session.execute(stmt)
    rows = result.all()
    if not rows:
        return None
    total_games = len(rows)
    total_played = sum(r[0].total_times_played for r in rows)
    total_wins = sum((r[0].wins or 0) for r in rows)
    win_rate = (total_wins / total_played) if total_played > 0 else 0.0
    sessions_this_week = await _sessions_used_this_week(session, user_id, tz_name)
    favorite = max(rows, key=lambda r: r[0].total_times_played)
    favorite_game = {
        "id": favorite[0].game_id,
        "gameName": favorite[1].game_name,
    }
    return {
        "totalGames": total_games,
        "winRate": round(win_rate, 4),
        "sessionsThisWeek": sessions_this_week,
        "favoriteGame": favorite_game,
    }


@router.get("/me", response_model=UserMeResponse)
async def get_me(
    _user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Current user profile and session quota (designers exempt from limit)."""
    db_user = await session.get(User, _user["id"])
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_error_body("unauthorized", "User not found"),
        )

    tz_name = db_user.time_zone or USER_TZ_DEFAULT
    used = await _sessions_used_this_week(session, db_user.id, tz_name)
    limit_val: int | None = None if db_user.designer else _get_session_limit_per_week()
    session_quota = SessionQuota(
        sessionsUsedThisWeek=used,
        sessionsLimitPerWeek=limit_val,
    )
    quick_stats = await _compute_quick_stats(session, db_user.id, tz_name)

    return UserMeResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        bio=db_user.bio,
        avatarUrl=db_user.avatar_url,
        designer=bool(db_user.designer),
        sessionQuota=session_quota,
        defaultSessionVisibility=db_user.default_session_visibility or "public",
        time_zone=db_user.time_zone,
        quickStats=quick_stats,
    )


@router.patch("/me", response_model=UserMeResponse)
async def update_me(
    body: UserMeUpdate,
    _user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Partial update of current user profile. 409 on duplicate username/email."""
    db_user = await session.get(User, _user["id"])
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_error_body("unauthorized", "User not found"),
        )

    if body.username is not None:
        stmt = select(User).where(
            User.username == body.username,
            User.id != db_user.id,
        )
        if (await session.execute(stmt)).scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=_error_body("validation_error", "Username already in use"),
            )
        db_user.username = body.username
    if body.email is not None:
        stmt = select(User).where(
            User.email == body.email,
            User.id != db_user.id,
        )
        if (await session.execute(stmt)).scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=_error_body("validation_error", "Email already in use"),
            )
        db_user.email = body.email
    if body.bio is not None:
        db_user.bio = body.bio
    if body.avatarUrl is not None:
        db_user.avatar_url = body.avatarUrl
    if body.time_zone is not None:
        db_user.time_zone = body.time_zone.strip() or None

    try:
        await session.commit()
        await session.refresh(db_user)
    except Exception:
        await session.rollback()
        raise

    tz_name = db_user.time_zone or USER_TZ_DEFAULT
    used = await _sessions_used_this_week(session, db_user.id, tz_name)
    limit_val = None if db_user.designer else _get_session_limit_per_week()
    session_quota = SessionQuota(
        sessionsUsedThisWeek=used,
        sessionsLimitPerWeek=limit_val,
    )
    quick_stats = await _compute_quick_stats(session, db_user.id, tz_name)

    return UserMeResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        bio=db_user.bio,
        avatarUrl=db_user.avatar_url,
        designer=bool(db_user.designer),
        sessionQuota=session_quota,
        defaultSessionVisibility=db_user.default_session_visibility or "public",
        time_zone=db_user.time_zone,
        quickStats=quick_stats,
    )


@router.get("/check-username", response_model=CheckUsernameResponse)
async def check_username(
    username: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_session),
):
    """Username availability (200, available true/false). No auth required."""
    stmt = select(User.id).where(User.username == username)
    result = await session.execute(stmt)
    exists = result.scalar_one_or_none() is not None
    return CheckUsernameResponse(available=not exists)


@router.get("/{user_id}", response_model=UserPublicResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Public profile of another user (no auth required per spec)."""
    db_user = await session.get(User, user_id)
    if not db_user:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "User not found"),
        )
    return UserPublicResponse(
        id=db_user.id,
        username=db_user.username,
        avatarUrl=db_user.avatar_url,
        bio=db_user.bio,
        designer=bool(db_user.designer),
        statsSummary=None,
    )
