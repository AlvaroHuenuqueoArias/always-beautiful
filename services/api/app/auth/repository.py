from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db.models import AdminUser, LoginAuditEvent, PasswordResetToken


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AuthRepository:
    def get_user_by_identifier(
        self,
        db: Session,
        identifier: str,
    ) -> Optional[AdminUser]:
        return db.scalar(
            select(AdminUser).where(
                or_(
                    AdminUser.username == identifier,
                    AdminUser.email == identifier,
                )
            )
        )

    def get_user_by_email(
        self,
        db: Session,
        email: str,
    ) -> Optional[AdminUser]:
        return db.scalar(select(AdminUser).where(AdminUser.email == email))

    def get_user_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> Optional[AdminUser]:
        return db.scalar(select(AdminUser).where(AdminUser.id == user_id))

    def create_login_audit_event(
        self,
        db: Session,
        *,
        user_id: int | None,
        identifier: str,
        event_type: str,
        success: bool,
        ip_address: str | None,
        request_id: str | None,
        user_agent: str | None,
        detail: str | None = None,
    ) -> LoginAuditEvent:
        event = LoginAuditEvent(
            user_id=user_id,
            identifier=identifier,
            event_type=event_type,
            success=success,
            ip_address=ip_address,
            request_id=request_id,
            user_agent=user_agent,
            detail=detail,
        )
        db.add(event)
        return event

    def count_recent_failed_login_attempts(
        self,
        db: Session,
        *,
        identifier: str,
        since: datetime,
    ) -> int:
        stmt = (
            select(func.count())  # pylint: disable=not-callable
            .select_from(LoginAuditEvent)
            .where(
                LoginAuditEvent.identifier == identifier,
                LoginAuditEvent.event_type == "login_failure",
                LoginAuditEvent.created_at >= since,
            )
        )
        return int(db.scalar(stmt) or 0)

    def invalidate_active_reset_tokens_for_user(
        self,
        db: Session,
        *,
        user_id: int,
    ) -> None:
        active_tokens = db.scalars(
            select(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.used_at.is_(None),
            )
        ).all()

        for item in active_tokens:
            item.used_at = utcnow()

    def create_password_reset_token(
        self,
        db: Session,
        *,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> PasswordResetToken:
        token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(token)
        return token

    def get_valid_password_reset_token(
        self,
        db: Session,
        *,
        token_hash: str,
    ) -> Optional[PasswordResetToken]:
        return db.scalar(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == token_hash,
                PasswordResetToken.used_at.is_(None),
            )
        )