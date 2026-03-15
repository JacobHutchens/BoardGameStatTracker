"""
Sessions routes: list, get, create, PATCH, DELETE, join, invites. Mounted at /v1/sessions.
DB-backed; session limit on create (designers exempt); visibility from override or creator default.
"""

import os
import secrets
import string
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select, func, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import (
    Game,
    GameTrackedStatSet,
    Scope,
    Session,
    SessionPlayer,
    SessionInvite,
    SessionTrackedStat,
    User,
    PlayerStatValue,
    TableStatValue,
)
from dependencies import get_current_user, pagination_params
from session_win_helpers import get_win_tracked_stat_id, get_player_won_value
from schemas_common import PaginationParams
from sessions.schemas import (
    SessionCreate,
    SessionCreateResponse,
    SessionInviteItem,
    SessionInviteListResponse,
    SessionListResponse,
    SessionPlayer as SessionPlayerSchema,
    SessionResponse,
    SessionUpdate,
    JoinRequest,
)

router = APIRouter()

DEFAULT_SESSION_LIMIT = 2
USER_TZ_DEFAULT = "America/Los_Angeles"


def _get_session_limit_per_week() -> int:
    raw = os.getenv("SESSION_LIMIT_PER_WEEK")
    if raw is None or raw == "":
        return DEFAULT_SESSION_LIMIT
    try:
        return max(1, int(raw))
    except ValueError:
        return DEFAULT_SESSION_LIMIT


def _week_bounds_utc(tz_name: str) -> tuple[datetime, datetime]:
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
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
    week_start, week_end = _week_bounds_utc(tz_name)
    stmt = select(func.count(Session.id)).where(
        Session.creator_user_id == user_id,
        Session.time_started >= week_start,
        Session.time_started <= week_end,
    )
    result = await session.execute(stmt)
    return result.scalar() or 0


def _error_body(code: str, message: str, details: list | None = None) -> dict:
    return {"error": {"code": code, "message": message}, "details": details or []}


def _dt_iso(s: datetime | None) -> str | None:
    if s is None:
        return None
    return s.isoformat() + "Z" if s.tzinfo is None else s.isoformat()


async def _build_session_response(
    session: AsyncSession,
    sess: Session,
    game: Game | None = None,
    stat_set: GameTrackedStatSet | None = None,
    creator: User | None = None,
) -> SessionResponse:
    if game is None:
        game = await session.get(Game, sess.game_id)
    if stat_set is None:
        stat_set = await session.get(GameTrackedStatSet, sess.stat_set_id)
    if creator is None:
        creator = await session.get(User, sess.creator_user_id)

    visibility = sess.visibility_override or (creator.default_session_visibility if creator else "public")

    # Load tracked stats for this session and build projection (statName, scope).
    stmt_st = select(SessionTrackedStat).where(SessionTrackedStat.session_id == sess.id)
    result_st = await session.execute(stmt_st)
    tracked_stat_rows = result_st.scalars().all()
    scope_ids = list({r.scope_id for r in tracked_stat_rows})
    scope_map = {}
    if scope_ids:
        stmt_scope = select(Scope).where(Scope.id.in_(scope_ids))
        for row in (await session.execute(stmt_scope)).scalars().all():
            scope_map[row.id] = row.scope or "player"
    tracked_stats_list = [
        {"statName": r.stat_name, "scope": scope_map.get(r.scope_id, "player")}
        for r in tracked_stat_rows
    ]

    win_tracked_stat_id = await get_win_tracked_stat_id(session, sess.id)

    stmt_players = select(SessionPlayer).where(SessionPlayer.session_id == sess.id)
    result_players = await session.execute(stmt_players)
    players_list = result_players.scalars().all()

    player_responses = []
    for sp in players_list:
        won_val = None
        if win_tracked_stat_id is not None:
            won_val = await get_player_won_value(session, sp.id, win_tracked_stat_id)
        player_responses.append(
            SessionPlayerSchema(
                sessionPlayerId=sp.id,
                userId=sp.user_id,
                playerName=sp.player_name,
                isSpectator=bool(sp.is_spectator),
                won=won_val,
            )
        )

    return SessionResponse(
        id=sess.id,
        sessionKey=sess.session_key,
        gameId=sess.game_id,
        game={"id": game.id, "gameName": game.game_name} if game else None,
        statSetId=sess.stat_set_id,
        statSet={"id": stat_set.id, "setName": stat_set.set_name} if stat_set else None,
        timeStarted=_dt_iso(sess.time_started) or "",
        timeEnded=_dt_iso(sess.time_ended),
        currentRound=sess.current_round,
        visibility=visibility or "public",
        players=player_responses,
        trackedStats=tracked_stats_list,
    )


async def _user_can_access_session(
    session: AsyncSession, session_id: int, user_id: int
) -> bool:
    stmt = select(Session).where(Session.id == session_id)
    result = await session.execute(stmt)
    sess = result.scalars().first()
    if not sess:
        return False
    if sess.creator_user_id == user_id:
        return True
    stmt_p = select(SessionPlayer).where(
        SessionPlayer.session_id == session_id,
        SessionPlayer.user_id == user_id,
    )
    return (await session.execute(stmt_p)).scalars().first() is not None


async def _generate_session_key(session: AsyncSession) -> str:
    for _ in range(20):
        key = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        stmt = select(Session.id).where(Session.session_key == key)
        if (await session.execute(stmt)).scalars().first() is None:
            return key
    raise RuntimeError("Could not generate unique session key")


@router.get("", response_model=SessionListResponse)
async def list_sessions(
    active: bool | None = Query(None),
    from_: str | None = Query(None, alias="from"),
    to: str | None = None,
    gameId: int | None = None,
    pagination: PaginationParams = Depends(pagination_params),
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """List sessions where current user is creator or participant. Filter by active, from/to, gameId."""
    user_id = current_user["id"]
    subq_creator = select(Session.id).where(Session.creator_user_id == user_id)
    subq_player = select(SessionPlayer.session_id).where(SessionPlayer.user_id == user_id)
    stmt = select(Session).where(or_(Session.id.in_(subq_creator), Session.id.in_(subq_player)))

    if active is not None:
        if active:
            stmt = stmt.where(Session.time_ended.is_(None))
        else:
            stmt = stmt.where(Session.time_ended.isnot(None))
    if from_:
        try:
            dt = datetime.fromisoformat(from_.replace("Z", "+00:00"))
            stmt = stmt.where(Session.time_started >= dt)
        except ValueError:
            pass
    if to:
        try:
            dt = datetime.fromisoformat(to.replace("Z", "+00:00"))
            stmt = stmt.where(Session.time_started <= dt)
        except ValueError:
            pass
    if gameId is not None:
        stmt = stmt.where(Session.game_id == gameId)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar() or 0

    stmt = stmt.order_by(Session.time_started.desc())
    stmt = stmt.offset((pagination.page - 1) * pagination.limit).limit(pagination.limit)
    result = await session.execute(stmt)
    sessions = result.scalars().all()

    out = []
    for sess in sessions:
        resp = await _build_session_response(session, sess)
        out.append(resp)

    return SessionListResponse(sessions=out, total=total, page=pagination.page)


@router.get("/invites", response_model=SessionInviteListResponse)
async def list_invites(
    pending: bool | None = Query(True),
    pagination: PaginationParams = Depends(pagination_params),
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """List session invites for current user. pending=true: active sessions not yet joined."""
    user_id = current_user["id"]
    stmt = (
        select(SessionInvite)
        .where(SessionInvite.user_id == user_id)
        .order_by(SessionInvite.invited_at.desc())
    )
    result = await session.execute(stmt)
    all_invites = result.scalars().all()

    if pending:
        filtered = []
        for inv in all_invites:
            sess = await session.get(Session, inv.session_id)
            if not sess or sess.time_ended is not None:
                continue
            stmt_p = select(SessionPlayer).where(
                SessionPlayer.session_id == inv.session_id,
                SessionPlayer.user_id == user_id,
            )
            if (await session.execute(stmt_p)).scalars().first() is not None:
                continue
            filtered.append(inv)
    else:
        filtered = all_invites

    total = len(filtered)
    start = (pagination.page - 1) * pagination.limit
    page_invites = filtered[start : start + pagination.limit]

    invite_items = []
    for inv in page_invites:
        sess = await session.get(Session, inv.session_id)
        game = await session.get(Game, sess.game_id) if sess else None
        stat_set = await session.get(GameTrackedStatSet, sess.stat_set_id) if sess else None
        creator = await session.get(User, sess.creator_user_id) if sess else None
        session_summary = None
        if sess and game:
            session_summary = {
                "id": sess.id,
                "sessionKey": sess.session_key,
                "gameId": sess.game_id,
                "game": {"id": game.id, "gameName": game.game_name},
                "statSetId": sess.stat_set_id,
                "statSet": {"id": stat_set.id, "setName": stat_set.set_name} if stat_set else None,
                "timeStarted": _dt_iso(sess.time_started),
                "creator": {"id": creator.id, "username": creator.username} if creator else None,
            }
        invite_items.append(
            SessionInviteItem(
                id=inv.id,
                sessionId=inv.session_id,
                invitedAt=inv.invited_at.isoformat() + "Z" if inv.invited_at.tzinfo is None else inv.invited_at.isoformat(),
                session=session_summary or {},
            )
        )

    return SessionInviteListResponse(invites=invite_items, total=total, page=pagination.page)


@router.post("/join", response_model=SessionResponse, status_code=status.HTTP_200_OK)
async def join_session(
    body: JoinRequest,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Join by session key. Idempotent if already in session. 404 not found, 409 if ended."""
    stmt = select(Session).where(Session.session_key == body.sessionKey)
    result = await session.execute(stmt)
    sess = result.scalars().first()
    if not sess:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Session not found"),
        )
    if sess.time_ended is not None:
        return JSONResponse(
            status_code=409,
            content=_error_body("conflict", "Session has already ended"),
        )

    stmt_p = select(SessionPlayer).where(
        SessionPlayer.session_id == sess.id,
        SessionPlayer.user_id == current_user["id"],
    )
    existing = (await session.execute(stmt_p)).scalars().first()
    if existing:
        return await _build_session_response(session, sess)

    session.add(
        SessionPlayer(
            session_id=sess.id,
            user_id=current_user["id"],
            player_name=current_user["username"],
            is_spectator=False,
        )
    )
    try:
        await session.commit()
        await session.refresh(sess)
    except Exception:
        await session.rollback()
        raise
    return await _build_session_response(session, sess)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session_detail(
    session_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Session details. 403 if not creator or participant, 404 if not found."""
    stmt = select(Session).where(Session.id == session_id)
    result = await session.execute(stmt)
    sess = result.scalars().first()
    if not sess:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Session not found"),
        )
    if not await _user_can_access_session(session, session_id, current_user["id"]):
        return JSONResponse(
            status_code=403,
            content=_error_body("forbidden", "You do not have access to this session"),
        )
    return await _build_session_response(session, sess)


@router.post("", response_model=SessionCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    body: SessionCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Create session. 403 if at weekly limit (designers exempt). 404 if game/stat set not found."""
    user_id = current_user["id"]
    game = await session.get(Game, body.gameId)
    if not game:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Game not found"),
        )
    stat_set = await session.get(GameTrackedStatSet, body.statSetId)
    if not stat_set or stat_set.game_id != body.gameId:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Stat set not found"),
        )

    user = await session.get(User, user_id)
    if not user:
        return JSONResponse(
            status_code=401,
            content=_error_body("unauthorized", "User not found"),
        )
    if not user.designer:
        tz_name = user.time_zone or USER_TZ_DEFAULT
        used = await _sessions_used_this_week(session, user_id, tz_name)
        limit = _get_session_limit_per_week()
        if used >= limit:
            return JSONResponse(
                status_code=403,
                content=_error_body("session_limit_exceeded", "Session limit for this week exceeded"),
            )

    session_key = await _generate_session_key(session)
    now = datetime.now(timezone.utc)

    new_sess = Session(
        creator_user_id=user_id,
        game_id=body.gameId,
        stat_set_id=body.statSetId,
        session_key=session_key,
        time_started=now,
        time_ended=None,
        current_round=1,
        visibility_override=None,
    )
    session.add(new_sess)
    await session.flush()

    session.add(
        SessionPlayer(
            session_id=new_sess.id,
            user_id=user_id,
            player_name=current_user["username"],
            is_spectator=False,
        )
    )
    for uid in body.invitedUserIds or []:
        if uid == user_id:
            continue
        session.add(
            SessionInvite(session_id=new_sess.id, user_id=uid, invited_at=now)
        )
    for name in body.nonAppPlayerNames or []:
        if name and name.strip():
            session.add(
                SessionPlayer(
                    session_id=new_sess.id,
                    user_id=None,
                    player_name=name.strip()[:45],
                    is_spectator=False,
                )
            )

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return SessionCreateResponse(sessionId=new_sess.id, sessionKey=new_sess.session_key)


@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: int,
    body: SessionUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """End session or update visibility. 403 if not creator/participant."""
    sess = await session.get(Session, session_id)
    if not sess:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Session not found"),
        )
    if not await _user_can_access_session(session, session_id, current_user["id"]):
        return JSONResponse(
            status_code=403,
            content=_error_body("forbidden", "You do not have access to this session"),
        )

    if body.timeEnded is not None:
        try:
            sess.time_ended = datetime.fromisoformat(body.timeEnded.replace("Z", "+00:00"))
        except ValueError:
            pass
    if body.visibilityOverride is not None:
        sess.visibility_override = body.visibilityOverride
    if body.status == "ended" and sess.time_ended is None:
        sess.time_ended = datetime.now(timezone.utc)

    try:
        await session.commit()
        await session.refresh(sess)
    except Exception:
        await session.rollback()
        raise
    return await _build_session_response(session, sess)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Delete session. 403 if not creator. 404 if not found."""
    sess = await session.get(Session, session_id)
    if not sess:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Session not found"),
        )
    if sess.creator_user_id != current_user["id"]:
        return JSONResponse(
            status_code=403,
            content=_error_body("forbidden", "Only the session creator can delete the session"),
        )

    players = (await session.execute(select(SessionPlayer).where(SessionPlayer.session_id == session_id))).scalars().all()
    player_ids = [sp.id for sp in players]
    if player_ids:
        await session.execute(delete(PlayerStatValue).where(PlayerStatValue.session_player_id.in_(player_ids)))
    await session.execute(delete(TableStatValue).where(TableStatValue.session_id == session_id))
    await session.execute(delete(SessionTrackedStat).where(SessionTrackedStat.session_id == session_id))
    await session.execute(delete(SessionInvite).where(SessionInvite.session_id == session_id))
    await session.execute(delete(SessionPlayer).where(SessionPlayer.session_id == session_id))
    await session.delete(sess)

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return Response(status_code=204)
