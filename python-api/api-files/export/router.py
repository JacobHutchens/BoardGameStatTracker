"""
Export routes: GET and POST /users/me/export. Query params comma-separated (gameIds, etc.). Mounted at /v1/users/me.
"""

from fastapi import APIRouter, Depends, Query

from dependencies import get_current_user
from export.schemas import ExportPostRequest, ExportPreviewResponse

router = APIRouter()


def _parse_comma_ids(value: str | None) -> list[int]:
    """Parse comma-separated ids from query or body."""
    if not value:
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip().isdigit()]


@router.get("/export")
def export_get(
    gameIds: str | None = Query(None),
    from_: str | None = Query(None, alias="from"),
    to: str | None = None,
    sessionIds: str | None = None,
    statSetIds: str | None = None,
    preview: bool = Query(False),
    _user=Depends(get_current_user),
):
    """Stub: GET export. Comma-separated array params. preview=true returns preview object."""
    if preview:
        return ExportPreviewResponse(
            sessionCount=0,
            statValueCount=0,
            estimatedSizeBytes=0,
        )
    return {"sessions": [], "stats": []}


@router.post("/export")
def export_post(
    body: ExportPostRequest | None = None,
    _user=Depends(get_current_user),
):
    """Stub: POST export with complex filters. preview=true returns preview object."""
    if body and body.preview:
        return ExportPreviewResponse(
            sessionCount=0,
            statValueCount=0,
            estimatedSizeBytes=0,
        )
    return {"sessions": [], "stats": []}
