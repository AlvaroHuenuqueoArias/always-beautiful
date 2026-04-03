from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.auth.repository import AuthRepository
from app.auth.security import decode_access_token
from app.db.models import AdminRole, AdminUser
from app.db.session import get_db


bearer_scheme = HTTPBearer(auto_error=False)
auth_repository = AuthRepository()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AdminUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = decode_access_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc

    subject = payload.get("sub")
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc

    user = auth_repository.get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


def require_admin_user(
    current_user: AdminUser = Depends(get_current_user),
) -> AdminUser:
    if current_user.role not in {
        AdminRole.ADMIN_OWNER,
        AdminRole.ADMIN_TECHNICAL,
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user


def require_admin_access(
    current_user: AdminUser = Depends(require_admin_user),
) -> AdminUser:
    return current_user


def require_admin_technical(
    current_user: AdminUser = Depends(get_current_user),
) -> AdminUser:
    if current_user.role != AdminRole.ADMIN_TECHNICAL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Technical administrator permissions are required",
        )
    return current_user