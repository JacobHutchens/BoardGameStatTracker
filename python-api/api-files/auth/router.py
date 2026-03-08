"""
Auth routes: login, register, publisher login, refresh, forgot-password, reset-password, logout.
All under /v1/auth (prefix applied in main).
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    ResetPasswordRequest,
    ResetPasswordResponse,
    UserSummary,
)
from database import get_session
from db_models import (
    User,
    UserRefreshToken,
    Publisher,
    PublisherRefreshToken,
)
from security import (
    ACCESS_TOKEN_TTL_SECONDS,
    REFRESH_TOKEN_TTL_DAYS,
    create_password_reset_token,
    create_publisher_access_token,
    create_user_access_token,
    hash_password,
    hash_refresh_token,
    mark_password_reset_token_used,
    validate_password_rules,
    verify_password,
    decode_password_reset_token,
)
from security import send_password_reset_email

router = APIRouter()

logout_security = HTTPBearer(auto_error=False)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _http_error(status_code: int, code: str, message: str, details: list[Any] | None = None) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error": {"code": code, "message": message}, "details": details or []},
    )


async def _issue_user_tokens(session: AsyncSession, user: User) -> tuple[str, str]:
    """Create access and refresh tokens for a user and persist the refresh token."""
    access_token = create_user_access_token(user.id)
    raw_refresh = os.urandom(32).hex()
    token_hash = hash_refresh_token(raw_refresh)
    now = _now_utc()
    refresh_entity = UserRefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=now + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
        revoked_at=None,
        created_at=now,
    )
    session.add(refresh_entity)
    return access_token, raw_refresh


async def _issue_publisher_tokens(session: AsyncSession, publisher: Publisher) -> tuple[str, str]:
    """Create access and refresh tokens for a publisher and persist the refresh token."""
    access_token = create_publisher_access_token(publisher.id)
    raw_refresh = os.urandom(32).hex()
    token_hash = hash_refresh_token(raw_refresh)
    now = _now_utc()
    refresh_entity = PublisherRefreshToken(
        publisher_id=publisher.id,
        token_hash=token_hash,
        expires_at=now + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
        revoked_at=None,
        created_at=now,
    )
    session.add(refresh_entity)
    return access_token, raw_refresh


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login(body: LoginRequest, session: AsyncSession = Depends(get_session)):
    """User login with emailOrUsername + password; returns access and refresh tokens."""
    # Look up by email first, then username
    stmt = select(User).where(User.email == body.emailOrUsername)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        stmt = select(User).where(User.username == body.emailOrUsername)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

    if user is None or not verify_password(body.password, user.password_hash):
        raise _http_error(status.HTTP_401_UNAUTHORIZED, "unauthorized", "Invalid credentials")

    try:
        access_token, refresh_token = await _issue_user_tokens(session, user)
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return AuthResponse(
        accessToken=access_token,
        refreshToken=refresh_token,
        expiresIn=ACCESS_TOKEN_TTL_SECONDS,
        user=UserSummary(id=user.id, username=user.username, email=user.email, designer=bool(user.designer)),
    )


@router.post("/register", response_model=AuthResponseRegister, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, session: AsyncSession = Depends(get_session)):
    """User registration with duplicate checks, password validation, and token issuance."""
    is_valid, msg = validate_password_rules(body.password)
    if not is_valid:
        raise _http_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "validation_error", msg or "Invalid password")

    # Check for duplicate username or email (use first() in case both match different users)
    stmt = select(User).where((User.username == body.username) | (User.email == body.email))
    result = await session.execute(stmt)
    existing = result.scalars().first()
    if existing:
        raise _http_error(
            status.HTTP_409_CONFLICT,
            "validation_error",
            "Username or email already in use",
        )

    now = _now_utc()
    user = User(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
        created_at=now,
        bio=None,
        avatar_url=None,
        designer=False,
        default_session_visibility="public",
        time_zone=None,
    )

    try:
        session.add(user)
        await session.flush()
        access_token, refresh_token = await _issue_user_tokens(session, user)
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return AuthResponseRegister(
        accessToken=access_token,
        refreshToken=refresh_token,
        expiresIn=ACCESS_TOKEN_TTL_SECONDS,
        user=UserSummary(id=user.id, username=user.username, email=user.email, designer=bool(user.designer)),
    )


@router.post("/publisher/login", response_model=PublisherAuthResponse, status_code=status.HTTP_200_OK)
async def publisher_login(body: LoginRequest, session: AsyncSession = Depends(get_session)):
    """Publisher login with emailOrUsername + password; returns access and refresh tokens."""
    stmt = select(Publisher).where(Publisher.email == body.emailOrUsername)
    result = await session.execute(stmt)
    publisher = result.scalar_one_or_none()
    if publisher is None:
        stmt = select(Publisher).where(Publisher.name == body.emailOrUsername)
        result = await session.execute(stmt)
        publisher = result.scalar_one_or_none()

    if publisher is None or not verify_password(body.password, publisher.password_hash):
        raise _http_error(status.HTTP_401_UNAUTHORIZED, "unauthorized", "Invalid credentials")

    try:
        access_token, refresh_token = await _issue_publisher_tokens(session, publisher)
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return PublisherAuthResponse(
        accessToken=access_token,
        refreshToken=refresh_token,
        expiresIn=ACCESS_TOKEN_TTL_SECONDS,
        publisher=PublisherSummary(id=publisher.id, name=publisher.name),
    )


@router.post("/refresh", response_model=RefreshResponse, status_code=status.HTTP_200_OK)
async def refresh(
    body: RefreshRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Exchange a valid refresh token for a new access token (and optionally a new refresh token).
    Looks up the refresh token in DB; revokes the old token and issues new access + refresh (rotation).
    Returns 401 if token is missing, invalid, revoked, or expired.
    """
    if not body.refreshToken or not body.refreshToken.strip():
        raise _http_error(status.HTTP_401_UNAUTHORIZED, "unauthorized", "Refresh token required")

    token_hash = hash_refresh_token(body.refreshToken)
    stmt = select(UserRefreshToken).where(UserRefreshToken.token_hash == token_hash)
    result = await session.execute(stmt)
    refresh_entity = result.scalars().first()
    if not refresh_entity:
        raise _http_error(status.HTTP_401_UNAUTHORIZED, "unauthorized", "Invalid refresh token")

    if refresh_entity.revoked_at is not None:
        raise _http_error(status.HTTP_401_UNAUTHORIZED, "unauthorized", "Refresh token has been revoked")

    now = _now_utc()
    if refresh_entity.expires_at < now:
        raise _http_error(status.HTTP_401_UNAUTHORIZED, "unauthorized", "Refresh token has expired")

    user = await session.get(User, refresh_entity.user_id)
    if not user:
        raise _http_error(status.HTTP_401_UNAUTHORIZED, "unauthorized", "User not found")

    # Rotate: revoke old token, issue new access + refresh
    refresh_entity.revoked_at = now
    access_token, raw_refresh = await _issue_user_tokens(session, user)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return RefreshResponse(
        accessToken=access_token,
        expiresIn=ACCESS_TOKEN_TTL_SECONDS,
        refreshToken=raw_refresh,
    )


@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
async def forgot_password(body: ForgotPasswordRequest, session: AsyncSession = Depends(get_session)):
    """
    Request password reset:
    - Always returns 200 with generic message.
    - If user exists, send a reset email via Gmail API.
    """
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        return ForgotPasswordResponse()

    try:
        base_url = os.getenv("PASSWORD_RESET_BASE_URL")
        if not base_url:
            raise RuntimeError("PASSWORD_RESET_BASE_URL is not configured.")

        token = create_password_reset_token(user.id)
        reset_link = f"{base_url.rstrip('/')}/reset-password?token={token}"
        await send_password_reset_email(user.email, reset_link)
    except RuntimeError as exc:
        # Misconfiguration or email failure: surface as 500 with clear message
        raise _http_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "internal_error",
            str(exc),
        )

    return ForgotPasswordResponse()


@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
async def reset_password(body: ResetPasswordRequest, session: AsyncSession = Depends(get_session)):
    """
    Reset password given a valid reset token and new password.
    - 200 on success.
    - 400 with specific error codes for invalid/expired/used tokens.
    - 422 for password validation failures.
    """
    # Validate password first
    is_valid, msg = validate_password_rules(body.newPassword)
    if not is_valid:
        raise _http_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "validation_error", msg or "Invalid password")

    try:
        data = decode_password_reset_token(body.token)
    except jwt.ExpiredSignatureError:
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "reset_token_expired",
            "Password reset token has expired",
        )
    except jwt.InvalidTokenError as exc:
        message = str(exc)
        code = "reset_token_used" if "already been used" in message else "invalid_reset_token"
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            code,
            "Invalid or already used password reset token",
        )

    user_id = data.get("sub")
    jti = data.get("jti")
    if not user_id or not jti:
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "invalid_reset_token",
            "Invalid password reset token payload",
        )

    try:
        user_id_int = int(user_id)
    except ValueError:
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "invalid_reset_token",
            "Invalid password reset token payload",
        )

    user = await session.get(User, user_id_int)
    if not user:
        raise _http_error(
            status.HTTP_400_BAD_REQUEST,
            "invalid_reset_token",
            "Invalid password reset token",
        )

    try:
        user.password_hash = hash_password(body.newPassword)
        await session.commit()
        mark_password_reset_token_used(str(jti))
    except Exception:
        await session.rollback()
        raise

    return ResetPasswordResponse()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    body: LogoutRequest | None = None,
    credentials: HTTPAuthorizationCredentials | None = Depends(logout_security),
    session: AsyncSession = Depends(get_session),
):
    """
    Hybrid logout:
    - If body.refreshToken is provided: revoke that specific token (user or publisher).
    - Else if Bearer token present: revoke all tokens for that user or publisher.
    - Always returns 204.
    """
    now = _now_utc()

    # Case 1: revoke a specific refresh token from body
    if body and body.refreshToken:
        token_hash = hash_refresh_token(body.refreshToken)
        # Try user tokens
        stmt_user = select(UserRefreshToken).where(UserRefreshToken.token_hash == token_hash)
        result_user = await session.execute(stmt_user)
        user_token = result_user.scalar_one_or_none()
        if user_token:
            user_token.revoked_at = now
            await session.commit()
            return None

        # Try publisher tokens
        stmt_pub = select(PublisherRefreshToken).where(PublisherRefreshToken.token_hash == token_hash)
        result_pub = await session.execute(stmt_pub)
        pub_token = result_pub.scalar_one_or_none()
        if pub_token:
            pub_token.revoked_at = now
            await session.commit()
            return None

        # Token not found: still 204 (nothing to revoke)
        return None

    # Case 2: no body token, but Bearer access token present -> revoke all for that principal
    if credentials and credentials.credentials:
        raw_token = credentials.credentials
        # Try user token
        try:
            data = jwt.decode(raw_token, os.getenv("JWT_SECRET", ""), algorithms=["HS256"])
            if data.get("type") == "user":
                user_id = int(data.get("sub"))
                stmt = select(UserRefreshToken).where(UserRefreshToken.user_id == user_id)
                result = await session.execute(stmt)
                tokens = result.scalars().all()
                for t in tokens:
                    t.revoked_at = now
                await session.commit()
                return None
        except Exception:
            pass

        # Try publisher token
        try:
            data = jwt.decode(raw_token, os.getenv("JWT_PUBLISHER_SECRET", ""), algorithms=["HS256"])
            if data.get("type") == "publisher":
                publisher_id = int(data.get("sub"))
                stmt = select(PublisherRefreshToken).where(PublisherRefreshToken.publisher_id == publisher_id)
                result = await session.execute(stmt)
                tokens = result.scalars().all()
                for t in tokens:
                    t.revoked_at = now
                await session.commit()
                return None
        except Exception:
            pass

    # Nothing to revoke, but logout is idempotent
    return None
