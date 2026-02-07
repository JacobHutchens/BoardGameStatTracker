"""
Pydantic response models for following feed.
"""

from pydantic import BaseModel
from typing import Any


class FeedSessionItem(BaseModel):
    id: int
    game: dict[str, Any]
    user: dict[str, Any]
    result: str | None = None  # derived won/lost
    playedAt: str
    visibility: str


class FeedResponse(BaseModel):
    sessions: list[FeedSessionItem]
    total: int
    page: int
