"""
Pydantic request/response models for stat sets (scoped to a game).
"""

from pydantic import BaseModel


class StatDefinition(BaseModel):
    id: int
    statName: str
    description: str = ""
    dataTypeId: int
    scopeId: int


class StatSetResponse(BaseModel):
    id: int
    gameId: int
    setName: str
    userId: int
    stats: list[StatDefinition]


class StatSetCreateStat(BaseModel):
    statName: str
    description: str = ""
    dataTypeId: int
    scopeId: int


class StatSetCreate(BaseModel):
    setName: str
    stats: list[StatSetCreateStat] | None = None
    sourceStatSetId: int | None = None


class StatSetListItem(BaseModel):
    id: int
    setName: str
    stats: list[dict]  # { statName, dataTypeId, scopeId }


class StatSetListResponse(BaseModel):
    statSets: list[StatSetListItem]
