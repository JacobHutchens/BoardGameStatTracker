"""
Feed route: GET /feed — sessions from followed users. Mounted at /v1.
Only sessions visible to current user (visibility = creator default + per-session override).
"""

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import Session, SessionPlayer, Follower, User, Game
from dependencies import get_current_user, pagination_params
from session_win_helpers import get_win_tracked_stat_id, get_player_won_value
from schemas_common import PaginationParams
from feed.schemas import FeedResponse, FeedSessionItem

router = APIRouter()


def _dt_iso(dt) -> str:
    if dt is None:
        return ""
    return dt.isoformat() + "Z" if getattr(dt, "tzinfo", None) is None else dt.isoformat()


@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    pagination: PaginationParams = Depends(pagination_params),
    since: str | None = Query(None),
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Sessions from users the current user follows; only public visibility. Optional since filter."""
    user_id = current_user["id"]
    following_subq = select(Follower.following_user_id).where(Follower.user_id == user_id)
    stmt = (
        select(Session)
        .join(User, Session.creator_user_id == User.id)
        .where(Session.creator_user_id.in_(following_subq))
        .where(Session.time_ended.isnot(None))
        .where(
            or_(
                Session.visibility_override == "public",
                and_(
                    Session.visibility_override.is_(None),
                    User.default_session_visibility == "public",
                ),
            )
        )
    )
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            stmt = stmt.where(Session.time_started >= since_dt)
        except ValueError:
            pass

    stmt = stmt.order_by(Session.time_started.desc())

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0

    stmt = stmt.offset((pagination.page - 1) * pagination.limit).limit(pagination.limit)
    result = await session.execute(stmt)
    sessions = result.scalars().unique().all()
    if not sessions:
        return FeedResponse(sessions=[], total=total, page=pagination.page)

    creator_ids = list({s.creator_user_id for s in sessions})
    users_stmt = select(User).where(User.id.in_(creator_ids))
    users_result = await session.execute(users_stmt)
    users_map = {u.id: u for u in users_result.scalars().all()}
    games_stmt = select(Game).where(Game.id.in_([s.game_id for s in sessions]))
    games_result = await session.execute(games_stmt)
    games_map = {g.id: g for g in games_result.scalars().all()}

    # Current user's participation and result (won/lost) per session.
    session_ids = [s.id for s in sessions]
    sp_stmt = select(SessionPlayer).where(
        SessionPlayer.session_id.in_(session_ids),
        SessionPlayer.user_id == user_id,
    )
    sp_result = await session.execute(sp_stmt)
    session_id_to_player = {sp.session_id: sp for sp in sp_result.scalars().all()}

    result_by_session = {}
    for sess in sessions:
        sp = session_id_to_player.get(sess.id)
        if sp is None:
            result_by_session[sess.id] = "other"
            continue
        win_stat_id = await get_win_tracked_stat_id(session, sess.id)
        if win_stat_id is None:
            result_by_session[sess.id] = "other"
            continue
        won_val = await get_player_won_value(session, sp.id, win_stat_id)
        if won_val is True:
            result_by_session[sess.id] = "won"
        elif won_val is False:
            result_by_session[sess.id] = "lost"
        else:
            result_by_session[sess.id] = "other"

    items = []
    for sess in sessions:
        creator = users_map.get(sess.creator_user_id)
        vis = sess.visibility_override or (creator.default_session_visibility if creator else "public")
        game = games_map.get(sess.game_id)
        items.append(
            FeedSessionItem(
                id=sess.id,
                game={"id": game.id, "gameName": game.game_name} if game else {},
                user={"id": creator.id, "username": creator.username} if creator else {},
                result=result_by_session.get(sess.id, "other"),
                playedAt=_dt_iso(sess.time_started),
                visibility=vis or "public",
            )
        )

    return FeedResponse(sessions=items, total=total, page=pagination.page)
