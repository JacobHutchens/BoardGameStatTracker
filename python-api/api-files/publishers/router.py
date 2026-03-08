"""
Publishers routes: GET me, GET me/designers, GET me/analytics, POST/DELETE me/designers. Mounted at /v1/publishers.
DB-backed; requires publisher auth.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import Publisher, PublisherDesigner, User, Session
from dependencies import get_current_publisher, pagination_params
from schemas_common import PaginationParams
from publishers.schemas import (
    AssignDesignerRequest,
    DesignerItem,
    DesignersListResponse,
    PublisherMeResponse,
)

router = APIRouter()


def _error_body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}, "details": []}


@router.get("/me", response_model=PublisherMeResponse)
async def get_publisher_me(
    session: AsyncSession = Depends(get_session),
    current_publisher: dict = Depends(get_current_publisher),
):
    """Publisher profile with designerTagCount and assignedCount from DB."""
    pub_id = current_publisher["id"]
    count_stmt = select(func.count(PublisherDesigner.id)).where(PublisherDesigner.publisher_id == pub_id)
    total_designers = (await session.execute(count_stmt)).scalar() or 0
    return PublisherMeResponse(
        id=pub_id,
        name=current_publisher["name"],
        designerTagCount=total_designers,
        assignedCount=total_designers,
    )


@router.get("/me/designers", response_model=DesignersListResponse)
async def list_designers(
    pagination: PaginationParams = Depends(pagination_params),
    session: AsyncSession = Depends(get_session),
    current_publisher: dict = Depends(get_current_publisher),
):
    """Users assigned designer tag by this publisher."""
    pub_id = current_publisher["id"]
    count_stmt = select(func.count(PublisherDesigner.id)).where(PublisherDesigner.publisher_id == pub_id)
    total = (await session.execute(count_stmt)).scalar() or 0

    stmt = (
        select(PublisherDesigner, User)
        .join(User, PublisherDesigner.user_id == User.id)
        .where(PublisherDesigner.publisher_id == pub_id)
        .order_by(PublisherDesigner.assigned_at.desc())
        .offset((pagination.page - 1) * pagination.limit)
        .limit(pagination.limit)
    )
    result = await session.execute(stmt)
    rows = result.all()
    designers = [
        DesignerItem(
            userId=row[0].user_id,
            username=row[1].username,
            assignedAt=row[0].assigned_at.isoformat() + "Z" if row[0].assigned_at.tzinfo is None else row[0].assigned_at.isoformat(),
        )
        for row in rows
    ]
    return DesignersListResponse(designers=designers, total=total, page=pagination.page)


@router.get("/me/analytics")
async def get_analytics(
    from_: str | None = Query(None, alias="from"),
    to: str | None = None,
    session: AsyncSession = Depends(get_session),
    current_publisher: dict = Depends(get_current_publisher),
):
    """Dashboard aggregates: sessions by designers, distinct games played in those sessions."""
    pub_id = current_publisher["id"]
    designer_user_ids = select(PublisherDesigner.user_id).where(PublisherDesigner.publisher_id == pub_id)
    from_dt = to_dt = None
    if from_:
        try:
            from_dt = datetime.fromisoformat(from_.replace("Z", "+00:00"))
        except ValueError:
            pass
    if to:
        try:
            to_dt = datetime.fromisoformat(to.replace("Z", "+00:00"))
        except ValueError:
            pass

    sessions_stmt = select(func.count(Session.id)).where(
        Session.creator_user_id.in_(designer_user_ids)
    )
    if from_dt:
        sessions_stmt = sessions_stmt.where(Session.time_started >= from_dt)
    if to_dt:
        sessions_stmt = sessions_stmt.where(Session.time_started <= to_dt)
    sessions_by_designers = (await session.execute(sessions_stmt)).scalar() or 0

    games_stmt = select(func.count(func.distinct(Session.game_id))).where(
        Session.creator_user_id.in_(designer_user_ids)
    )
    if from_dt:
        games_stmt = games_stmt.where(Session.time_started >= from_dt)
    if to_dt:
        games_stmt = games_stmt.where(Session.time_started <= to_dt)
    games_created = (await session.execute(games_stmt)).scalar() or 0

    return {
        "sessionsByDesigners": sessions_by_designers,
        "gamesCreated": games_created,
    }


@router.post("/me/designers", status_code=status.HTTP_201_CREATED)
async def assign_designer(
    body: AssignDesignerRequest,
    session: AsyncSession = Depends(get_session),
    current_publisher: dict = Depends(get_current_publisher),
):
    """Assign designer tag to user. 201 or 204; 404 if user not found; 409 if already assigned."""
    pub_id = current_publisher["id"]
    user = await session.get(User, body.userId)
    if not user:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "User not found"),
        )
    stmt = select(PublisherDesigner).where(
        PublisherDesigner.publisher_id == pub_id,
        PublisherDesigner.user_id == body.userId,
    )
    existing = (await session.execute(stmt)).scalars().first()
    if existing:
        return Response(status_code=204)

    session.add(
        PublisherDesigner(
            publisher_id=pub_id,
            user_id=body.userId,
            assigned_at=datetime.now(timezone.utc),
        )
    )
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return Response(status_code=201)


@router.delete("/me/designers/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_designer(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_publisher: dict = Depends(get_current_publisher),
):
    """Revoke designer tag. 404 if not assigned."""
    pub_id = current_publisher["id"]
    result = await session.execute(
        delete(PublisherDesigner).where(
            PublisherDesigner.publisher_id == pub_id,
            PublisherDesigner.user_id == user_id,
        )
    )
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    if result.rowcount == 0:
        return JSONResponse(
            status_code=404,
            content=_error_body("not_found", "Designer assignment not found"),
        )
    return Response(status_code=204)
