"""
Stub auth and shared dependencies.
- Accept any Bearer token; return a minimal user or publisher for dependency injection.
- Pagination: default page=1, limit=20, max limit=50.
"""

from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from schemas_common import PaginationParams

# Default and max for pagination (per design)
DEFAULT_PAGE = 1
DEFAULT_LIMIT = 20
MAX_LIMIT = 50

security = HTTPBearer(auto_error=False)


def _stub_user_from_token(credentials: HTTPAuthorizationCredentials | None) -> dict[str, Any] | None:
    """Stub: any Bearer token yields a mock user. No token => None."""
    if not credentials or not credentials.credentials:
        return None
    return {
        "id": 1,
        "username": "stub_user",
        "email": "stub@example.com",
        "designer": False,
    }


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> dict[str, Any]:
    """Require auth: raise 401 if no Bearer token. Stub: accept any token."""
    user = _stub_user_from_token(credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "unauthorized", "message": "Missing or invalid token"}, "details": []},
        )
    return user


def get_current_user_optional(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> dict[str, Any] | None:
    """Optional auth: return stub user if Bearer present, else None."""
    return _stub_user_from_token(credentials)


def get_current_publisher(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> dict[str, Any]:
    """Require publisher auth. Stub: any Bearer token yields a mock publisher."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "unauthorized", "message": "Missing or invalid token"}, "details": []},
        )
    return {
        "id": 1,
        "name": "Stub Publisher",
        "designerTagCount": 5,
        "assignedCount": 3,
    }


def pagination_params(
    page: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT,
) -> PaginationParams:
    """Parse and clamp pagination: page >= 1, limit in [1, MAX_LIMIT]."""
    page = max(1, page)
    limit = max(1, min(MAX_LIMIT, limit))
    return PaginationParams(page=page, limit=limit)
