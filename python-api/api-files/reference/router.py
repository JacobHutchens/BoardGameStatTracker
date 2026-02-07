"""
Reference data routes: GET /scopes, GET /data-types. Public (no auth).
"""

from fastapi import APIRouter

from reference.schemas import DataTypeItem, DataTypesResponse, ScopeItem, ScopesResponse

router = APIRouter()


@router.get("/scopes", response_model=ScopesResponse)
def list_scopes():
    """Stub: return mock scopes (e.g. player, table)."""
    return ScopesResponse(
        scopes=[
            ScopeItem(id=1, scope="player"),
            ScopeItem(id=2, scope="table"),
        ]
    )


@router.get("/data-types", response_model=DataTypesResponse)
def list_data_types():
    """Stub: return mock data types (e.g. integer, string, boolean)."""
    return DataTypesResponse(
        dataTypes=[
            DataTypeItem(id=1, dataType="integer"),
            DataTypeItem(id=2, dataType="string"),
            DataTypeItem(id=3, dataType="boolean"),
        ]
    )
