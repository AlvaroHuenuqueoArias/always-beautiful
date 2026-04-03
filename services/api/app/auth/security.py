from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import get_settings


password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(
    *,
    subject: str,
    role: str,
    expires_delta: timedelta | None = None,
) -> tuple[str, int]:
    settings = get_settings()
    now = datetime.utcnow()
    expire = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )

    payload = {
        "sub": subject,
        "role": role,
        "type": "access",
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )
    expires_in = int((expire - now).total_seconds())
    return encoded_jwt, expires_in


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except InvalidTokenError as exc:
        raise credentials_exception from exc

    if payload.get("type") != "access" or payload.get("sub") is None:
        raise credentials_exception

    return payload


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()