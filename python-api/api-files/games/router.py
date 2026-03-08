"""
Games routes: GET list, GET by id, POST create.
DB-backed; 201 + full game on create; 409 on duplicate name (per design guide).
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import Game, GameTrackedStatSet, Session, SessionPlayer
from dependencies import get_current_user_optional, pagination_params
from schemas_common import PaginationParams
from games.schemas import GameCreate, GameResponse, GameListResponse

router = APIRouter()


def _game_to_response(g: Game, play_count: int | None = None, last_played_at: datetime | None = None) -> GameResponse:
    """Map DB Game to API GameResponse. ISO datetime for createdAt."""
    return GameResponse(
        id=g.id,
        gameName=g.game_name,
        description=g.description or "",
        minPlayerCount=g.min_player_count or 0,
        maxPlayerCount=g.max_player_count or 0,
        canWin=bool(g.can_win),
        createdAt=g.created_at.isoformat() + "Z" if g.created_at.tzinfo is None else g.created_at.isoformat(),
        playCount=play_count,
        lastPlayedAt=last_played_at.isoformat() + "Z" if last_played_at and last_played_at.tzinfo is None else (last_played_at.isoformat() if last_played_at else None),
    )


def _error_body(code: str, message: str, details: list | None = None) -> dict:
    return {"error": {"code": code, "message": message}, "details": details or []}


@router.get("", response_model=GameListResponse)
async def list_games(
    filter_: str | None = Query(None, alias="filter"),
    search: str | None = None,
    pagination: PaginationParams = Depends(pagination_params),
    session: AsyncSession = Depends(get_session),
    current_user: dict | None = Depends(get_current_user_optional),
):
    """
    List games with optional filter (my|all|recent) and search.
    my = user has played or created a stat set; recent = games with session in last 30 days.
    """
    stmt = select(Game)
    # Filter: my | all | recent
    if filter_ == "my" and current_user:
        user_id = current_user["id"]
        # Games where user created a stat set OR participated in a session
        subq_stat_set = select(GameTrackedStatSet.game_id).where(GameTrackedStatSet.user_id == user_id)
        subq_played = (
            select(Session.game_id)
            .select_from(Session)
            .join(SessionPlayer, Session.id == SessionPlayer.session_id)
            .where(SessionPlayer.user_id == user_id)
        )
        stmt = stmt.where(or_(Game.id.in_(subq_stat_set), Game.id.in_(subq_played)))
    elif filter_ == "recent":
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        subq_recent = select(Session.game_id).where(Session.time_started >= cutoff)
        stmt = stmt.where(Game.id.in_(subq_recent))
    # else filter_ == "all" or None: no extra filter

    if search and search.strip():
        pattern = f"%{search.strip()}%"
        stmt = stmt.where(Game.game_name.like(pattern))

    # Count total (same filters)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await session.execute(count_stmt)
    total = total_result.scalar() or 0

    stmt = stmt.order_by(Game.created_at.desc())
    stmt = stmt.offset((pagination.page - 1) * pagination.limit).limit(pagination.limit)
    result = await session.execute(stmt)
    games = result.scalars().all()

    return GameListResponse(
        games=[_game_to_response(g) for g in games],
        total=total,
        page=pagination.page,
    )


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Game details by id; 404 if not found."""
    game = await session.get(Game, game_id)
    if not game:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Game not found"),
        )
    return _game_to_response(game)


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(
    body: GameCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create game; 409 if a game with the same name already exists."""
    stmt = select(Game).where(Game.game_name == body.gameName)
    result = await session.execute(stmt)
    existing = result.scalars().first()
    if existing:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=_error_body(
                "game_already_exists",
                f"A game with the name '{body.gameName}' already exists (id={existing.id}).",
                details=[{"existingGameId": existing.id, "existingGameName": existing.game_name}],
            ),
        )

    now = datetime.now(timezone.utc)
    game = Game(
        game_name=body.gameName,
        description=body.description or "",
        min_player_count=body.minPlayerCount,
        max_player_count=body.maxPlayerCount,
        can_win=body.canWin,
        created_at=now,
    )
    session.add(game)
    try:
        await session.commit()
        await session.refresh(game)
    except Exception:
        await session.rollback()
        raise

    return _game_to_response(game)
