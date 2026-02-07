"""
Publishers routes: GET me, GET me/designers, GET me/analytics, POST/DELETE me/designers. Mounted at /v1/publishers.
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from dependencies import get_current_publisher, pagination_params
from schemas_common import PaginationParams
from publishers.schemas import (
    AssignDesignerRequest,
    DesignerItem,
    DesignersListResponse,
    PublisherMeResponse,
)

router = APIRouter()


@router.get("/me", response_model=PublisherMeResponse)
def get_publisher_me(_pub=Depends(get_current_publisher)):
    """Stub: publisher profile."""
    return PublisherMeResponse(**_pub)


@router.get("/me/designers", response_model=DesignersListResponse)
def list_designers(
    pagination: PaginationParams = Depends(pagination_params),
    _pub=Depends(get_current_publisher),
):
    """Stub: users assigned designer tag."""
    return DesignersListResponse(
        designers=[
            DesignerItem(userId=1, username="stub_designer", assignedAt="2025-01-01T00:00:00Z"),
        ],
        total=1,
        page=pagination.page,
    )


@router.get("/me/analytics")
def get_analytics(
    from_: str | None = None,
    to: str | None = None,
    _pub=Depends(get_current_publisher),
):
    """Stub: dashboard aggregates (sessions by designers, games created, etc.)."""
    return {
        "sessionsByDesigners": 0,
        "gamesCreated": 0,
    }


@router.post("/me/designers", status_code=201)
def assign_designer(body: AssignDesignerRequest, _pub=Depends(get_current_publisher)):
    """Stub: assign designer tag. 201 or 204; 409 if already assigned."""
    return Response(status_code=201)


@router.delete("/me/designers/{user_id}", status_code=204)
def revoke_designer(user_id: int, _pub=Depends(get_current_publisher)):
    """Stub: revoke designer tag. 404 if not found."""
    return Response(status_code=204)
