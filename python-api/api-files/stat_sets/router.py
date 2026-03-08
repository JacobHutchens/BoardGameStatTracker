"""
Stat sets routes: GET list, GET by id, POST create.
Mounted at /v1/games/{game_id}/stat-sets. DB-backed; 404 if game or stat set missing.
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import Game, GameTrackedStatSet, GameTrackedStat
from dependencies import get_current_user
from stat_sets.schemas import (
    StatSetCreate,
    StatSetCreateStat,
    StatSetListItem,
    StatSetListResponse,
    StatSetResponse,
    StatDefinition,
)

router = APIRouter()


def _error_body(code: str, message: str, details: list | None = None) -> dict:
    return {"error": {"code": code, "message": message}, "details": details or []}


async def _ensure_game_exists(session: AsyncSession, game_id: int) -> bool:
    """Return True if game exists."""
    game = await session.get(Game, game_id)
    return game is not None


@router.get("", response_model=StatSetListResponse)
async def list_stat_sets(
    game_id: int,
    session: AsyncSession = Depends(get_session),
):
    """List stat sets for the game. 404 if game not found."""
    if not await _ensure_game_exists(session, game_id):
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Game not found"),
        )

    stmt = select(GameTrackedStatSet).where(GameTrackedStatSet.game_id == game_id)
    result = await session.execute(stmt)
    sets = result.scalars().all()

    if not sets:
        return StatSetListResponse(statSets=[])

    set_ids = [s.id for s in sets]
    stmt_stats = select(GameTrackedStat).where(
        GameTrackedStat.game_tracked_stat_set_id.in_(set_ids)
    )
    result_stats = await session.execute(stmt_stats)
    stats_list = result_stats.scalars().all()

    stats_by_set: dict[int, list[GameTrackedStat]] = {}
    for s in stats_list:
        stats_by_set.setdefault(s.game_tracked_stat_set_id, []).append(s)

    return StatSetListResponse(
        statSets=[
            StatSetListItem(
                id=s.id,
                setName=s.set_name,
                stats=[
                    {
                        "statName": st.stat_name,
                        "dataTypeId": st.data_type_id,
                        "scopeId": st.scope_id,
                    }
                    for st in stats_by_set.get(s.id, [])
                ],
            )
            for s in sets
        ]
    )


@router.get("/{stat_set_id}", response_model=StatSetResponse)
async def get_stat_set(
    game_id: int,
    stat_set_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Stat set details. 404 if game or stat set not found."""
    if not await _ensure_game_exists(session, game_id):
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Game not found"),
        )

    stmt = select(GameTrackedStatSet).where(
        GameTrackedStatSet.game_id == game_id,
        GameTrackedStatSet.id == stat_set_id,
    )
    result = await session.execute(stmt)
    stat_set = result.scalars().first()
    if not stat_set:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Stat set not found"),
        )

    stmt_stats = select(GameTrackedStat).where(
        GameTrackedStat.game_tracked_stat_set_id == stat_set_id
    )
    result_stats = await session.execute(stmt_stats)
    stats = result_stats.scalars().all()

    return StatSetResponse(
        id=stat_set.id,
        gameId=stat_set.game_id,
        setName=stat_set.set_name,
        userId=stat_set.user_id,
        stats=[
            StatDefinition(
                id=st.id,
                statName=st.stat_name,
                description=st.description or "",
                dataTypeId=st.data_type_id,
                scopeId=st.scope_id,
            )
            for st in stats
        ],
    )


@router.post("", response_model=StatSetResponse, status_code=status.HTTP_201_CREATED)
async def create_stat_set(
    game_id: int,
    body: StatSetCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Create stat set (optionally copy from sourceStatSetId). 404 if game or source not found."""
    if not await _ensure_game_exists(session, game_id):
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Game not found"),
        )

    user_id = current_user["id"]
    stats_to_create: list[tuple[str, str, int, int]] = []  # (stat_name, description, data_type_id, scope_id)

    if body.sourceStatSetId is not None:
        stmt = select(GameTrackedStatSet).where(
            GameTrackedStatSet.id == body.sourceStatSetId,
            GameTrackedStatSet.game_id == game_id,
        )
        result = await session.execute(stmt)
        source_set = result.scalars().first()
        if not source_set:
            return JSONResponse(
                status_code=404,
                content=_error_body("not_found", "Stat set not found"),
            )
        stmt_stats = select(GameTrackedStat).where(
            GameTrackedStat.game_tracked_stat_set_id == source_set.id
        )
        result_stats = await session.execute(stmt_stats)
        for st in result_stats.scalars().all():
            stats_to_create.append(
                (st.stat_name, st.description or "", st.data_type_id, st.scope_id)
            )
    elif body.stats:
        for st in body.stats:
            stats_to_create.append(
                (st.statName, st.description or "", st.dataTypeId, st.scopeId)
            )

    if not stats_to_create:
        stats_to_create = [("score", "", 1, 1)]

    new_set = GameTrackedStatSet(
        game_id=game_id,
        user_id=user_id,
        set_name=body.setName,
    )
    session.add(new_set)
    await session.flush()

    for stat_name, description, data_type_id, scope_id in stats_to_create:
        session.add(
            GameTrackedStat(
                game_tracked_stat_set_id=new_set.id,
                stat_name=stat_name,
                description=description or None,
                data_type_id=data_type_id,
                scope_id=scope_id,
            )
        )

    try:
        await session.commit()
        await session.refresh(new_set)
    except Exception:
        await session.rollback()
        raise

    stmt_stats = select(GameTrackedStat).where(
        GameTrackedStat.game_tracked_stat_set_id == new_set.id
    )
    result_stats = await session.execute(stmt_stats)
    stats = result_stats.scalars().all()

    return StatSetResponse(
        id=new_set.id,
        gameId=new_set.game_id,
        setName=new_set.set_name,
        userId=new_set.user_id,
        stats=[
            StatDefinition(
                id=st.id,
                statName=st.stat_name,
                description=st.description or "",
                dataTypeId=st.data_type_id,
                scopeId=st.scope_id,
            )
            for st in stats
        ],
    )
