"""
Export routes: GET and POST /users/me/export. Query params comma-separated or body. Mounted at /v1/users/me.
DB-backed: sessions where current user participated; filter by gameIds, from/to, sessionIds, statSetIds.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import Session, SessionPlayer, PlayerStatValue, TableStatValue
from dependencies import get_current_user
from export.schemas import ExportPostRequest, ExportPreviewResponse

router = APIRouter()


def _parse_comma_ids(value: str | None) -> list[int]:
    if not value:
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip().isdigit()]


def _parse_date(s: str | None):
    if not s:
        return None
    try:
        from datetime import datetime
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def _export_base_query(user_id: int, game_ids: list[int], from_dt, to_dt, session_ids: list[int], stat_set_ids: list[int]):
    """Sessions where user is creator or in session_player, with optional filters."""
    subq_player = select(SessionPlayer.session_id).where(SessionPlayer.user_id == user_id)
    stmt = select(Session).where(
        (Session.creator_user_id == user_id) | (Session.id.in_(subq_player))
    )
    if game_ids:
        stmt = stmt.where(Session.game_id.in_(game_ids))
    if from_dt:
        stmt = stmt.where(Session.time_started >= from_dt)
    if to_dt:
        stmt = stmt.where(Session.time_started <= to_dt)
    if session_ids:
        stmt = stmt.where(Session.id.in_(session_ids))
    if stat_set_ids:
        stmt = stmt.where(Session.stat_set_id.in_(stat_set_ids))
    return stmt


@router.get("/export")
async def export_get(
    gameIds: str | None = Query(None),
    from_: str | None = Query(None, alias="from"),
    to: str | None = None,
    sessionIds: str | None = None,
    statSetIds: str | None = None,
    preview: bool = Query(False),
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """GET export. Comma-separated params. preview=true returns counts; else export JSON."""
    user_id = current_user["id"]
    game_ids = _parse_comma_ids(gameIds)
    session_ids = _parse_comma_ids(sessionIds)
    stat_set_ids = _parse_comma_ids(statSetIds)
    from_dt = _parse_date(from_)
    to_dt = _parse_date(to)
    if from_dt and to_dt and from_dt > to_dt:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": {"code": "validation_error", "message": "Invalid date range"}, "details": []},
        )

    stmt = _export_base_query(user_id, game_ids, from_dt, to_dt, session_ids, stat_set_ids)
    result = await session.execute(stmt)
    sessions = result.scalars().all()
    session_id_list = [s.id for s in sessions]

    if preview:
        session_count = len(session_id_list)
        stat_value_count = 0
        if session_id_list:
            player_ids_stmt = select(SessionPlayer.id).where(SessionPlayer.session_id.in_(session_id_list))
            player_ids = (await session.execute(player_ids_stmt)).scalars().all()
            if player_ids:
                pv = (await session.execute(select(func.count(PlayerStatValue.id)).where(PlayerStatValue.session_player_id.in_(player_ids)))).scalar() or 0
                stat_value_count += pv
            tv = (await session.execute(select(func.count(TableStatValue.id)).where(TableStatValue.session_id.in_(session_id_list)))).scalar() or 0
            stat_value_count += tv
        estimated = session_count * 500 + stat_value_count * 50
        return ExportPreviewResponse(
            sessionCount=session_count,
            statValueCount=stat_value_count,
            estimatedSizeBytes=estimated,
        )

    out_sessions = [
        {"id": s.id, "sessionKey": s.session_key, "gameId": s.game_id, "statSetId": s.stat_set_id, "timeStarted": s.time_started.isoformat() if s.time_started else None, "timeEnded": s.time_ended.isoformat() if s.time_ended else None}
        for s in sessions
    ]
    stats_out = []
    if session_id_list:
        pids = (await session.execute(select(SessionPlayer.id).where(SessionPlayer.session_id.in_(session_id_list)))).scalars().all()
        if pids:
            pv_stmt = select(PlayerStatValue).where(PlayerStatValue.session_player_id.in_(pids))
            for row in (await session.execute(pv_stmt)).scalars().all():
                stats_out.append({"sessionPlayerId": row.session_player_id, "statValue": row.stat_value, "recordedAt": row.recorded_at.isoformat() if row.recorded_at else None})
        tv_stmt = select(TableStatValue).where(TableStatValue.session_id.in_(session_id_list))
        for row in (await session.execute(tv_stmt)).scalars().all():
            stats_out.append({"sessionId": row.session_id, "statValue": row.stat_value, "recordedAt": row.recorded_at.isoformat() if row.recorded_at else None})
    return {"sessions": out_sessions, "stats": stats_out}


@router.post("/export")
async def export_post(
    body: ExportPostRequest | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """POST export with body filters. preview=true returns preview object."""
    user_id = current_user["id"]
    if not body:
        body = ExportPostRequest()
    game_ids = body.gameIds or []
    session_ids = body.sessionIds or []
    stat_set_ids = body.statSetIds or []
    from_dt = _parse_date(body.from_)
    to_dt = _parse_date(body.to)
    if from_dt and to_dt and from_dt > to_dt:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": {"code": "validation_error", "message": "Invalid date range"}, "details": []},
        )

    stmt = _export_base_query(user_id, game_ids, from_dt, to_dt, session_ids, stat_set_ids)
    result = await session.execute(stmt)
    sessions = result.scalars().all()
    session_id_list = [s.id for s in sessions]

    if body.preview:
        session_count = len(session_id_list)
        stat_value_count = 0
        if session_id_list:
            player_ids = (await session.execute(select(SessionPlayer.id).where(SessionPlayer.session_id.in_(session_id_list)))).scalars().all()
            if player_ids:
                stat_value_count += (await session.execute(select(func.count(PlayerStatValue.id)).where(PlayerStatValue.session_player_id.in_(player_ids)))).scalar() or 0
            stat_value_count += (await session.execute(select(func.count(TableStatValue.id)).where(TableStatValue.session_id.in_(session_id_list)))).scalar() or 0
        return ExportPreviewResponse(
            sessionCount=session_count,
            statValueCount=stat_value_count,
            estimatedSizeBytes=session_count * 500 + stat_value_count * 50,
        )

    out_sessions = [
        {"id": s.id, "sessionKey": s.session_key, "gameId": s.game_id, "statSetId": s.stat_set_id, "timeStarted": s.time_started.isoformat() if s.time_started else None, "timeEnded": s.time_ended.isoformat() if s.time_ended else None}
        for s in sessions
    ]
    stats_out = []
    if session_id_list:
        pids = (await session.execute(select(SessionPlayer.id).where(SessionPlayer.session_id.in_(session_id_list)))).scalars().all()
        if pids:
            for row in (await session.execute(select(PlayerStatValue).where(PlayerStatValue.session_player_id.in_(pids)))).scalars().all():
                stats_out.append({"sessionPlayerId": row.session_player_id, "statValue": row.stat_value, "recordedAt": row.recorded_at.isoformat() if row.recorded_at else None})
        for row in (await session.execute(select(TableStatValue).where(TableStatValue.session_id.in_(session_id_list)))).scalars().all():
            stats_out.append({"sessionId": row.session_id, "statValue": row.stat_value, "recordedAt": row.recorded_at.isoformat() if row.recorded_at else None})
    return {"sessions": out_sessions, "stats": stats_out}
