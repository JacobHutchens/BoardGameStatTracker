"""
Shared dependencies: auth (JWT + DB-backed current user/publisher) and pagination.
- Pagination: default page=1, limit=20, max limit=50.
"""

from typing import Annotated, Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from schemas_common import PaginationParams
from database import get_session
from db_models import User, Publisher
from security import (
    decode_user_access_token,
    decode_publisher_access_token,
)

# Default and max for pagination (per design)
DEFAULT_PAGE = 1
DEFAULT_LIMIT = 20
MAX_LIMIT = 50

security = HTTPBearer(auto_error=False)


def _unauthorized_error(message: str = "Missing or invalid token") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": {"code": "unauthorized", "message": message}, "details": []},
    )


async def _get_bearer_credentials(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> Optional[str]:
    if not credentials or not credentials.credentials:
        return None
    if credentials.scheme.lower() != "bearer":
        return None
    return credentials.credentials


async def get_current_user(
    token: Annotated[Optional[str], Depends(_get_bearer_credentials)],
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """
    Require auth: decode JWT using JWT_SECRET, load user from DB, or 401.
    Returns a lightweight dict compatible with existing routers.
    """
    if not token:
        raise _unauthorized_error()

    try:
        payload = decode_user_access_token(token)
    except Exception:
        raise _unauthorized_error("Invalid access token")

    user_id = payload.get("sub")
    if user_id is None:
        raise _unauthorized_error("Invalid access token payload")

    try:
        user_id_int = int(user_id)
    except ValueError:
        raise _unauthorized_error("Invalid access token payload")

    db_user = await session.get(User, user_id_int)
    if not db_user:
        raise _unauthorized_error("User not found")

    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "designer": bool(db_user.designer),
    }


async def get_current_user_optional(
    token: Annotated[Optional[str], Depends(_get_bearer_credentials)],
    session: AsyncSession = Depends(get_session),
) -> Optional[dict[str, Any]]:
    """
    Optional auth: return user dict if a valid Bearer token is present, else None.
    Invalid tokens still raise 401 to avoid silent failures.
    """
    if not token:
        return None

    try:
        payload = decode_user_access_token(token)
    except Exception:
        raise _unauthorized_error("Invalid access token")

    user_id = payload.get("sub")
    if user_id is None:
        raise _unauthorized_error("Invalid access token payload")

    try:
        user_id_int = int(user_id)
    except ValueError:
        raise _unauthorized_error("Invalid access token payload")

    db_user = await session.get(User, user_id_int)
    if not db_user:
        raise _unauthorized_error("User not found")

    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "designer": bool(db_user.designer),
    }


async def get_current_publisher(
    token: Annotated[Optional[str], Depends(_get_bearer_credentials)],
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """
    Require publisher auth: decode JWT with JWT_PUBLISHER_SECRET and load publisher from DB.
    """
    if not token:
        raise _unauthorized_error()

    try:
        payload = decode_publisher_access_token(token)
    except Exception:
        raise _unauthorized_error("Invalid access token")

    publisher_id = payload.get("sub")
    if publisher_id is None:
        raise _unauthorized_error("Invalid access token payload")

    try:
        publisher_id_int = int(publisher_id)
    except ValueError:
        raise _unauthorized_error("Invalid access token payload")

    db_publisher = await session.get(Publisher, publisher_id_int)
    if not db_publisher:
        raise _unauthorized_error("Publisher not found")

    return {
        "id": db_publisher.id,
        "name": db_publisher.name,
        "designerTagCount": 0,
        "assignedCount": 0,
    }


def pagination_params(
    page: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT,
) -> PaginationParams:
    """Parse and clamp pagination: page >= 1, limit in [1, MAX_LIMIT]."""
    page = max(1, page)
    limit = max(1, min(MAX_LIMIT, limit))
    return PaginationParams(page=page, limit=limit)
