"""Password hashing (bcrypt) + JWT token encode/decode. Core security primitives."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import hashlib
import uuid

from ..config import settings


def hash_password(plain: str) -> str:
    # bcrypt has a 72-byte limit (not 72 characters). Version the pre-hash
    # scheme while retaining verification of existing hashes.
    value = hashlib.sha256(plain.encode()).hexdigest().encode()
    return "sha256$" + bcrypt.hashpw(value, bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    if hashed.startswith("sha256$"):
        return bcrypt.checkpw(
            hashlib.sha256(plain.encode()).hexdigest().encode(), hashed[7:].encode()
        )
    return bcrypt.checkpw(plain.encode()[:72], hashed.encode())


def _encode(
    sub: str, token_type: str, ttl: timedelta, extra: dict | None = None
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "type": token_type,
        "iat": now,
        "exp": now + ttl,
        "jti": uuid.uuid4().hex,
        **(extra or {}),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def make_access_token(user_id: int, role: str, version: int = 0) -> str:
    return _encode(
        str(user_id),
        "access",
        timedelta(minutes=settings.access_token_ttl_min),
        {"role": role, "ver": version},
    )


def make_refresh_token(user_id: int) -> str:
    return _encode(
        str(user_id),
        "refresh",
        timedelta(days=settings.refresh_token_ttl_days),
    )


def decode_token(token: str, expected_type: str) -> dict:
    """Giải mã + verify. Raise jwt.InvalidTokenError nếu hỏng/hết hạn/sai type."""
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["sub", "exp", "iat"]},
    )
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError(f"expected {expected_type} token")
    if not str(payload["sub"]).isdigit():
        raise jwt.InvalidTokenError("invalid subject")
    return payload
