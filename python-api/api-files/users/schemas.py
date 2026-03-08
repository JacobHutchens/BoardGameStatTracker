"""
Pydantic request/response models for users and profile.
"""

from pydantic import BaseModel
from typing import Any


class SessionQuota(BaseModel):
    sessionsUsedThisWeek: int
    sessionsLimitPerWeek: int | None  # null = unlimited (designer)


class UserMeResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: str | None = None
    avatarUrl: str | None = None
    designer: bool
    sessionQuota: SessionQuota
    defaultSessionVisibility: str = "public"
    time_zone: str | None = None  # optional IANA timezone (per design doc)
    quickStats: dict[str, Any] | None = None


class UserMeUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    bio: str | None = None
    avatarUrl: str | None = None
    time_zone: str | None = None  # IANA timezone e.g. America/Los_Angeles; null or "" to clear


class UserPublicResponse(BaseModel):
    id: int
    username: str
    avatarUrl: str | None = None
    bio: str | None = None
    designer: bool
    statsSummary: dict[str, Any] | None = None


class CheckUsernameResponse(BaseModel):
    available: bool
