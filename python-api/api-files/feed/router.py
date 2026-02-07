"""
Feed route: GET /feed — sessions from followed users. Mounted at /v1.
"""

from fastapi import APIRouter, Depends

from dependencies import get_current_user, pagination_params
from schemas_common import PaginationParams
from feed.schemas import FeedResponse, FeedSessionItem

router = APIRouter()


@router.get("/feed", response_model=FeedResponse)
def get_feed(
    pagination: PaginationParams = Depends(pagination_params),
    since: str | None = None,
    _user=Depends(get_current_user),
):
    """Stub: sessions from followed users (visibility = user default + per-session)."""
    return FeedResponse(
        sessions=[
            FeedSessionItem(
                id=1,
                game={"id": 1, "gameName": "Stub Game"},
                user={"id": 1, "username": "stub_user"},
                result="Won",
                playedAt="2025-01-01T12:00:00Z",
                visibility="public",
            )
        ],
        total=1,
        page=pagination.page,
    )
