"""
Pydantic request/response models for publishers.
"""

from pydantic import BaseModel


class PublisherMeResponse(BaseModel):
    id: int
    name: str
    designerTagCount: int
    assignedCount: int


class DesignerItem(BaseModel):
    userId: int
    username: str
    assignedAt: str


class DesignersListResponse(BaseModel):
    designers: list[DesignerItem]
    total: int
    page: int


class AssignDesignerRequest(BaseModel):
    userId: int
