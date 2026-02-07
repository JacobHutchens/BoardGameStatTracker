"""
Shared Pydantic schemas: error body and pagination response wrapper.
API error shape: { "error": { "code", "message" }, "details": [] }
"""

from pydantic import BaseModel, Field


class ErrorPart(BaseModel):
    """Error code and message inside the standard error response."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Standard API error body for 4xx/5xx responses."""

    error: ErrorPart
    details: list = Field(default_factory=list)


class PaginationParams(BaseModel):
    """Parsed pagination: page (1-based), limit (capped at max_limit)."""

    page: int = 1
    limit: int = 20
