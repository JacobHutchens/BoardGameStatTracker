"""
Auth routes: login, register, publisher login, refresh, forgot-password, logout.
All under /v1/auth (prefix applied in main).
"""

from fastapi import APIRouter, status

from auth.schemas import (
    AuthResponse,
    AuthResponseRegister,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    LogoutRequest,
    PublisherAuthResponse,
    PublisherSummary,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    UserSummary,
)
from dependencies import get_current_user_optional

router = APIRouter()


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(body: LoginRequest):
    """Stub: accept any credentials, return mock tokens and user."""
    return AuthResponse(
        accessToken="stub_access_token",
        refreshToken="stub_refresh_token",
        expiresIn=3600,
        user=UserSummary(id=1, username="stub_user", email="stub@example.com", designer=False),
    )


@router.post("/register", response_model=AuthResponseRegister, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    """Stub: accept any body, return mock tokens and user (no duplicate check)."""
    return AuthResponseRegister(
        accessToken="stub_access_token",
        refreshToken="stub_refresh_token",
        expiresIn=3600,
        user=UserSummary(id=1, username=body.username, email=body.email, designer=False),
    )


@router.post("/publisher/login", response_model=PublisherAuthResponse, status_code=status.HTTP_200_OK)
def publisher_login(body: LoginRequest):
    """Stub: accept any credentials, return mock publisher tokens."""
    return PublisherAuthResponse(
        accessToken="stub_publisher_token",
        refreshToken="stub_publisher_refresh",
        expiresIn=3600,
        publisher=PublisherSummary(id=1, name="Stub Publisher"),
    )


@router.post("/refresh", response_model=RefreshResponse, status_code=status.HTTP_200_OK)
def refresh(body: RefreshRequest):
    """Stub: accept any refresh token, return new access token."""
    return RefreshResponse(accessToken="stub_access_token", expiresIn=3600)


@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
def forgot_password(body: ForgotPasswordRequest):
    """Stub: always return 200 with generic message (no email leak)."""
    return ForgotPasswordResponse()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(body: LogoutRequest | None = None):
    """Stub: optional body with refreshToken; return 204."""
    return None
