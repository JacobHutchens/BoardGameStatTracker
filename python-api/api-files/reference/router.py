"""
Reference data routes: GET /scopes, GET /data-types. Public (no auth). DB-backed.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from db_models import Scope, DataType
from reference.schemas import DataTypeItem, DataTypesResponse, ScopeItem, ScopesResponse

router = APIRouter()


@router.get("/scopes", response_model=ScopesResponse)
async def list_scopes(session: AsyncSession = Depends(get_session)):
    """Return all scopes from DB (e.g. player, table)."""
    result = await session.execute(select(Scope).order_by(Scope.id))
    scopes = result.scalars().all()
    return ScopesResponse(
        scopes=[ScopeItem(id=s.id, scope=s.scope) for s in scopes]
    )


@router.get("/data-types", response_model=DataTypesResponse)
async def list_data_types(session: AsyncSession = Depends(get_session)):
    """Return all data types from DB (e.g. integer, string, boolean)."""
    result = await session.execute(select(DataType).order_by(DataType.id))
    data_types = result.scalars().all()
    return DataTypesResponse(
        dataTypes=[
            DataTypeItem(id=d.id, dataType=d.data_type or "")
            for d in data_types
        ]
    )
