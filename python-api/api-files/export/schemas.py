"""
Pydantic request/response models for export (preview and filters).
"""

from pydantic import BaseModel, Field


class ExportPreviewResponse(BaseModel):
    sessionCount: int
    statValueCount: int
    estimatedSizeBytes: int


class ExportPostRequest(BaseModel):
    gameIds: list[int] = []
    from_: str | None = Field(None, alias="from")
    to: str | None = None
    sessionIds: list[int] = []
    statSetIds: list[int] = []
    preview: bool = False
