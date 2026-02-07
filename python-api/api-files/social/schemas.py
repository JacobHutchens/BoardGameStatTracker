"""
Pydantic response models for followers, following, user search.
"""

from pydantic import BaseModel


class FollowerItem(BaseModel):
    id: int
    username: str


class FollowersResponse(BaseModel):
    followers: list[FollowerItem]
    total: int
    page: int


class FollowingResponse(BaseModel):
    following: list[FollowerItem]
    total: int
    page: int


class UserSearchItem(BaseModel):
    id: int
    username: str


class UserSearchResponse(BaseModel):
    users: list[UserSearchItem]
    total: int
    page: int
