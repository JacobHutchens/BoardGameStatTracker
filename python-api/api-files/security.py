from __future__ import annotations

import base64
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from typing import Any, Dict, Optional, Set, Tuple

import httpx
import jwt
from argon2 import PasswordHasher


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------


def _get_env_strict(name: str) -> str:
    """
    Read an environment variable and fail fast if missing or empty.

    Edge case rule: use os.getenv(name, "") and raise a clear error if empty
    when auth / email functionality is used.
    """
    value = os.getenv(name, "")
    if not value:
        raise RuntimeError(f"Required environment variable '{name}' is not set or empty.")
    return value


def _get_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


# Token TTLs (seconds / days)
ACCESS_TOKEN_TTL_SECONDS = _get_int_env("ACCESS_TOKEN_TTL_SECONDS", 3600)
REFRESH_TOKEN_TTL_DAYS = _get_int_env("REFRESH_TOKEN_TTL_DAYS", 30)
PASSWORD_RESET_TOKEN_TTL_SECONDS = _get_int_env("PASSWORD_RESET_TOKEN_TTL_SECONDS", 3600)


# ---------------------------------------------------------------------------
# Password hashing (argon2)
# ---------------------------------------------------------------------------

_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a password using argon2."""
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against an argon2 hash."""
    try:
        return _password_hasher.verify(password_hash, password)
    except Exception:
        return False


def validate_password_rules(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password against ImplementationSpec rules:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 number
    - At least 1 special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    if not any(not c.isalnum() for c in password):
        return False, "Password must contain at least one special character."
    return True, None


# ---------------------------------------------------------------------------
# JWT creation / verification (access tokens)
# ---------------------------------------------------------------------------


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _create_jwt(payload: Dict[str, Any], secret_env_name: str, ttl_seconds: int) -> str:
    secret = _get_env_strict(secret_env_name)
    now = _utcnow()
    to_encode = {
        **payload,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl_seconds)).timestamp()),
    }
    return jwt.encode(to_encode, secret, algorithm="HS256")


def _decode_jwt(token: str, secret_env_name: str) -> Dict[str, Any]:
    secret = _get_env_strict(secret_env_name)
    return jwt.decode(token, secret, algorithms=["HS256"])


def create_user_access_token(user_id: int, extra: Optional[Dict[str, Any]] = None) -> str:
    payload: Dict[str, Any] = {"sub": str(user_id), "type": "user"}
    if extra:
        payload.update(extra)
    return _create_jwt(payload, "JWT_SECRET", ACCESS_TOKEN_TTL_SECONDS)


def decode_user_access_token(token: str) -> Dict[str, Any]:
    data = _decode_jwt(token, "JWT_SECRET")
    if data.get("type") != "user":
        raise jwt.InvalidTokenError("Invalid token type for user.")
    return data


def create_publisher_access_token(publisher_id: int, extra: Optional[Dict[str, Any]] = None) -> str:
    payload: Dict[str, Any] = {"sub": str(publisher_id), "type": "publisher"}
    if extra:
        payload.update(extra)
    return _create_jwt(payload, "JWT_PUBLISHER_SECRET", ACCESS_TOKEN_TTL_SECONDS)


def decode_publisher_access_token(token: str) -> Dict[str, Any]:
    data = _decode_jwt(token, "JWT_PUBLISHER_SECRET")
    if data.get("type") != "publisher":
        raise jwt.InvalidTokenError("Invalid token type for publisher.")
    return data


# ---------------------------------------------------------------------------
# Refresh token helpers (opaque string + hash stored in DB)
# ---------------------------------------------------------------------------


def generate_refresh_token() -> str:
    """Generate a new opaque refresh token string."""
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    """Hash a refresh token for storage using deterministic SHA-256 (no plaintext)."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_refresh_token(token: str, token_hash: str) -> bool:
    """Verify a refresh token against its stored hash."""
    return hash_refresh_token(token) == token_hash


# ---------------------------------------------------------------------------
# Password-reset JWT + in-memory used set
# ---------------------------------------------------------------------------

_used_password_reset_jti: Set[str] = set()


def create_password_reset_token(user_id: int) -> str:
    """
    Short-lived JWT for password reset.
    Claims:
      - sub: user id
      - purpose: "password_reset"
      - jti: random id for used-token tracking
    """
    jti = secrets.token_urlsafe(16)
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "purpose": "password_reset",
        "jti": jti,
    }
    return _create_jwt(payload, "JWT_SECRET", PASSWORD_RESET_TOKEN_TTL_SECONDS)


def decode_password_reset_token(token: str) -> Dict[str, Any]:
    """Decode and validate a password-reset JWT, without checking 'used' status."""
    data = _decode_jwt(token, "JWT_SECRET")
    if data.get("purpose") != "password_reset":
        raise jwt.InvalidTokenError("Invalid token purpose for password reset.")
    jti = data.get("jti")
    if not jti:
        raise jwt.InvalidTokenError("Missing jti in password reset token.")
    if jti in _used_password_reset_jti:
        raise jwt.InvalidTokenError("Password reset token has already been used.")
    return data


def mark_password_reset_token_used(jti: str) -> None:
    """Mark a password-reset token jti as used (in-memory only)."""
    _used_password_reset_jti.add(jti)


# ---------------------------------------------------------------------------
# Gmail-based password reset email sender
# ---------------------------------------------------------------------------


async def send_password_reset_email(email: str, reset_link: str) -> None:
    """
    Send a password reset email using the Gmail REST API.

    This uses a pre-configured OAuth2 access token and sender address:
      - GMAIL_SENDER: email address to send from (e.g. boardgamestats@example.com)
      - GMAIL_ACCESS_TOKEN: OAuth 2.0 access token with gmail.send scope
      - GMAIL_API_BASE_URL: optional override (default: https://gmail.googleapis.com)

    If these are not configured, a clear error is raised so the deployer can
    provide real credentials.
    """
    sender = _get_env_strict("GMAIL_SENDER")
    access_token = _get_env_strict("GMAIL_ACCESS_TOKEN")
    base_url = os.getenv("GMAIL_API_BASE_URL", "https://gmail.googleapis.com").rstrip("/")

    subject = "Reset your Board Game Stat Tracker password"
    body = (
        "You requested a password reset for your Board Game Stat Tracker account.\n\n"
        f"Click this link to reset your password:\n{reset_link}\n\n"
        "If you did not request this, you can safely ignore this email."
    )

    message = EmailMessage()
    message["To"] = email
    message["From"] = sender
    message["Subject"] = subject
    message.set_content(body)

    raw_bytes = message.as_bytes()
    raw_b64 = base64.urlsafe_b64encode(raw_bytes).decode("utf-8")

    url = f"{base_url}/gmail/v1/users/{sender}/messages/send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"raw": raw_b64}

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise RuntimeError(
                f"Gmail API error while sending password reset email: "
                f"status={resp.status_code}, body={resp.text[:200]}"
            )

