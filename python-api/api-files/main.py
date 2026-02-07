"""
The Librarian — Board Game Stat Tracker REST API.
All routes under /v1. Stub auth; central exception handlers; response shape per api-documentation.
"""
import sys
from pathlib import Path

# Ensure api-files directory is on path so subpackages can import dependencies, schemas_common
_sys_path = str(Path(__file__).resolve().parent)
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from schemas_common import ErrorResponse, ErrorPart

# Routers
from auth.router import router as auth_router
from reference.router import router as reference_router
from games.router import router as games_router
from stat_sets.router import router as stat_sets_router
from sessions.router import router as sessions_router
from users.router import router as users_router
from stats.router import router as stats_router
from social.router import router as social_router
from feed.router import router as feed_router
from export.router import router as export_router
from publishers.router import router as publishers_router

app = FastAPI(
    title="The Librarian",
    description="Board Game Stat Tracker REST API — stub implementation with mock data.",
    version="1.0",
)


def _error_body(code: str, message: str, details: list | None = None) -> dict:
    return {"error": {"code": code, "message": message}, "details": details or []}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Ensure HTTPException responses use API error shape."""
    detail = exc.detail
    if isinstance(detail, dict) and "error" in detail:
        return JSONResponse(status_code=exc.status_code, content=detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body("error", str(detail) if detail else "An error occurred", []),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Map Pydantic validation errors to API error shape."""
    errors = exc.errors() if hasattr(exc, "errors") else []
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_body("validation_error", "Request validation failed", errors),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch-all for 5xx; return standard error shape."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_body("internal_error", "An unexpected error occurred", []),
    )


# Include routers under /v1
app.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
app.include_router(reference_router, prefix="/v1", tags=["reference"])
# Reference routes are at /v1/scopes and /v1/data-types (router defines /scopes, /data-types)
# So we need reference at /v1 and router has paths /scopes, /data-types
# Actually reference router has @router.get("/scopes") and @router.get("/data-types") - so prefix /v1 gives /v1/scopes, /v1/data-types. But then we'd have no prefix for "reference" - so we mount reference_router with prefix "/v1" and the router defines /scopes and /data-types. So we get /v1/scopes and /v1/data-types. Good.

# Games at /v1/games
app.include_router(games_router, prefix="/v1/games", tags=["games"])

# Stat sets under /v1/games/{game_id}/stat-sets
app.include_router(stat_sets_router, prefix="/v1/games/{game_id}/stat-sets", tags=["stat_sets"])

# Sessions at /v1/sessions
app.include_router(sessions_router, prefix="/v1/sessions", tags=["sessions"])

# Social (include before users so /v1/users/search matches before /v1/users/{user_id})
app.include_router(social_router, prefix="/v1/users", tags=["social"])
# Users at /v1/users (router has /me, /{user_id}, /check-username)
app.include_router(users_router, prefix="/v1/users", tags=["users"])

# Stats: /v1/users/me/stats, /v1/users/{user_id}/stats, /v1/games/{game_id}/stats
app.include_router(stats_router, prefix="/v1", tags=["stats"])

# Feed at /v1/feed
app.include_router(feed_router, prefix="/v1", tags=["feed"])

# Export at /v1/users/me/export
app.include_router(export_router, prefix="/v1/users/me", tags=["export"])

# Publishers at /v1/publishers
app.include_router(publishers_router, prefix="/v1/publishers", tags=["publishers"])
