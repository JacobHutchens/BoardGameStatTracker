"""
Social routes: GET followers/following, POST/DELETE follow, GET users/search. Mounted at /v1/users.
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, Response

from dependencies import get_current_user, pagination_params
from schemas_common import PaginationParams
from social.schemas import FollowerItem, FollowersResponse, FollowingResponse, UserSearchItem, UserSearchResponse

router = APIRouter()


@router.get("/search", response_model=UserSearchResponse)
def search_users(
    q: str = Query(...),
    pagination: PaginationParams = Depends(pagination_params),
):
    """Stub: search users by query string."""
    page = pagination.page
    limit = pagination.limit
    return UserSearchResponse(
        users=[UserSearchItem(id=1, username="stub_user")],
        total=1,
        page=page,
    )


@router.get("/{user_id}/followers", response_model=FollowersResponse)
def list_followers(
    user_id: int,
    pagination: PaginationParams = Depends(pagination_params),
    search: str | None = None,
):
    """Stub: list followers of user. 404 if user not found."""
    return FollowersResponse(
        followers=[FollowerItem(id=1, username="stub_follower")],
        total=1,
        page=pagination.page,
    )


@router.get("/{user_id}/following", response_model=FollowingResponse)
def list_following(
    user_id: int,
    pagination: PaginationParams = Depends(pagination_params),
    search: str | None = None,
):
    """Stub: list users that user follows."""
    return FollowingResponse(
        following=[FollowerItem(id=1, username="stub_user")],
        total=1,
        page=pagination.page,
    )


@router.post("/{user_id}/follow", status_code=204)
def follow_user(user_id: int, _user=Depends(get_current_user)):
    """Stub: follow user (idempotent). 404 if user not found."""
    return Response(status_code=204)


@router.delete("/{user_id}/follow", status_code=204)
def unfollow_user(user_id: int, _user=Depends(get_current_user)):
    """Stub: unfollow. 404 if user not found."""
    return Response(status_code=204)
