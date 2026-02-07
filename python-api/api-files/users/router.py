"""
Users routes: GET/PATCH /me, GET /{user_id}, GET /check-username. Mounted at /v1/users.
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from dependencies import get_current_user
from users.schemas import CheckUsernameResponse, UserMeResponse, UserMeUpdate, UserPublicResponse, SessionQuota

router = APIRouter()


@router.get("/me", response_model=UserMeResponse)
def get_me(_user=Depends(get_current_user)):
    """Stub: current user profile and session quota."""
    return UserMeResponse(
        id=_user["id"],
        username=_user["username"],
        email=_user["email"],
        bio=None,
        avatarUrl=None,
        designer=_user.get("designer", False),
        sessionQuota=SessionQuota(sessionsUsedThisWeek=0, sessionsLimitPerWeek=10),
        defaultSessionVisibility="public",
        quickStats={"totalGames": 0, "winRate": 0.0, "sessionsThisWeek": 0, "favoriteGame": None},
    )


@router.patch("/me", response_model=UserMeResponse)
def update_me(body: UserMeUpdate, _user=Depends(get_current_user)):
    """Stub: partial update of profile. 409 on duplicate username/email."""
    return UserMeResponse(
        id=_user["id"],
        username=body.username or _user["username"],
        email=body.email or _user["email"],
        bio=body.bio,
        avatarUrl=body.avatarUrl,
        designer=_user.get("designer", False),
        sessionQuota=SessionQuota(sessionsUsedThisWeek=0, sessionsLimitPerWeek=10),
        defaultSessionVisibility="public",
    )


@router.get("/check-username", response_model=CheckUsernameResponse)
def check_username(username: str = Query(...)):
    """Stub: username availability (200, available true/false)."""
    return CheckUsernameResponse(available=(username != "taken"))


@router.get("/{user_id}", response_model=UserPublicResponse)
def get_user(user_id: int):
    """Stub: public profile of another user (no auth required per spec for public view)."""
    if user_id == 1:
        return UserPublicResponse(
            id=1,
            username="stub_user",
            avatarUrl=None,
            bio=None,
            designer=False,
            statsSummary={},
        )
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "not_found", "message": "User not found"}, "details": []},
    )
