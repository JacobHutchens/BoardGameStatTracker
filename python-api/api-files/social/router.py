"""
Social routes: GET followers/following, POST/DELETE follow, GET users/search. Mounted at /v1/users.
DB-backed; 404 if user not found where applicable.
"""

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse, Response
from datetime import datetime, timezone
from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import User, Follower
from dependencies import get_current_user, pagination_params
from schemas_common import PaginationParams
from social.schemas import (
    FollowerItem,
    FollowersResponse,
    FollowingResponse,
    UserSearchItem,
    UserSearchResponse,
)

router = APIRouter()


def _error_body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}, "details": []}


async def _user_exists(session: AsyncSession, user_id: int) -> bool:
    return (await session.get(User, user_id)) is not None


@router.get("/search", response_model=UserSearchResponse)
async def search_users(
    q: str = Query(..., min_length=1),
    pagination: PaginationParams = Depends(pagination_params),
    session: AsyncSession = Depends(get_session),
):
    """Search users by username (and optionally email). No auth required."""
    pattern = f"%{q.strip()}%"
    stmt = select(User).where(User.username.like(pattern)).order_by(User.username)
    count_stmt = select(func.count()).select_from(
        select(User).where(User.username.like(pattern)).subquery()
    )
    total = (await session.execute(count_stmt)).scalar() or 0
    stmt = stmt.offset((pagination.page - 1) * pagination.limit).limit(pagination.limit)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return UserSearchResponse(
        users=[UserSearchItem(id=u.id, username=u.username) for u in users],
        total=total,
        page=pagination.page,
    )


@router.get("/{user_id}/followers", response_model=FollowersResponse)
async def list_followers(
    user_id: int,
    pagination: PaginationParams = Depends(pagination_params),
    search: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    """List followers of user (users who follow this user). 404 if user not found."""
    if not await _user_exists(session, user_id):
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "User not found"),
        )
    # Follower: user_id = follower, following_user_id = followed. Followers of user_id = Follower where following_user_id = user_id.
    subq = (
        select(Follower.user_id)
        .where(Follower.following_user_id == user_id)
    )
    stmt = select(User).where(User.id.in_(subq))
    if search and search.strip():
        stmt = stmt.where(User.username.like(f"%{search.strip()}%"))
    stmt = stmt.order_by(User.username)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0
    stmt = stmt.offset((pagination.page - 1) * pagination.limit).limit(pagination.limit)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return FollowersResponse(
        followers=[FollowerItem(id=u.id, username=u.username) for u in users],
        total=total,
        page=pagination.page,
    )


@router.get("/{user_id}/following", response_model=FollowingResponse)
async def list_following(
    user_id: int,
    pagination: PaginationParams = Depends(pagination_params),
    search: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    """List users that this user follows. 404 if user not found."""
    if not await _user_exists(session, user_id):
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "User not found"),
        )
    subq = select(Follower.following_user_id).where(Follower.user_id == user_id)
    stmt = select(User).where(User.id.in_(subq))
    if search and search.strip():
        stmt = stmt.where(User.username.like(f"%{search.strip()}%"))
    stmt = stmt.order_by(User.username)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0
    stmt = stmt.offset((pagination.page - 1) * pagination.limit).limit(pagination.limit)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return FollowingResponse(
        following=[FollowerItem(id=u.id, username=u.username) for u in users],
        total=total,
        page=pagination.page,
    )


@router.post("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Follow user (idempotent). 404 if user not found. Cannot follow self."""
    if user_id == current_user["id"]:
        return Response(status_code=204)
    if not await _user_exists(session, user_id):
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "User not found"),
        )
    stmt = select(Follower).where(
        Follower.user_id == current_user["id"],
        Follower.following_user_id == user_id,
    )
    existing = (await session.execute(stmt)).scalars().first()
    if existing:
        return Response(status_code=204)
    session.add(
        Follower(
            user_id=current_user["id"],
            following_user_id=user_id,
            followed_at=datetime.now(timezone.utc),
        )
    )
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return Response(status_code=204)


@router.delete("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Unfollow. 404 if user not found. Idempotent."""
    if not await _user_exists(session, user_id):
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "User not found"),
        )
    await session.execute(
        delete(Follower).where(
            Follower.user_id == current_user["id"],
            Follower.following_user_id == user_id,
        )
    )
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return Response(status_code=204)
