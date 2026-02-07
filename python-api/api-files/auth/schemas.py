"""
Pydantic request/response models for auth and user/publisher summary.
"""

from pydantic import BaseModel, Field


# ----- Request bodies -----
class LoginRequest(BaseModel):
    emailOrUsername: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class RefreshRequest(BaseModel):
    refreshToken: str


class ForgotPasswordRequest(BaseModel):
    email: str


class LogoutRequest(BaseModel):
    refreshToken: str | None = None


# ----- User summary (in login/register response) -----
class UserSummary(BaseModel):
    id: int
    username: str
    email: str
    designer: bool


# ----- Publisher summary (in publisher login response) -----
class PublisherSummary(BaseModel):
    id: int
    name: str


# ----- Responses -----
class AuthResponse(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int
    user: UserSummary


class AuthResponseRegister(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int
    user: UserSummary


class PublisherAuthResponse(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int
    publisher: PublisherSummary


class RefreshResponse(BaseModel):
    accessToken: str
    expiresIn: int


class ForgotPasswordResponse(BaseModel):
    message: str = "If an account exists, you will receive reset instructions."
