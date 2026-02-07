"""
Pydantic response models for reference data: scopes and data types.
"""

from pydantic import BaseModel


class ScopeItem(BaseModel):
    id: int
    scope: str


class ScopesResponse(BaseModel):
    scopes: list[ScopeItem]


class DataTypeItem(BaseModel):
    id: int
    dataType: str


class DataTypesResponse(BaseModel):
    dataTypes: list[DataTypeItem]
