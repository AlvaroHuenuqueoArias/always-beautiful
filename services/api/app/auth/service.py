from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.repository import AuthRepository
from app.auth.schemas import (
    CurrentUserResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    MessageResponse,
    ResetPasswordRequest,
    TokenResponse,
)
from app.auth.security import (
    create_access_token,
    generate_reset_token,
    get_password_hash,
    hash_reset_token,
    verify_password,
)
from app.core.config import get_settings
from app.db.models import AdminUser


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def normalize_to_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository
        self.settings = get_settings()

    def login(
        self,
        db: Session,
        *,
        payload: LoginRequest,
        request: Request,
    ) -> TokenResponse:
        identifier = payload.identifier.strip().lower()
        request_id = getattr(request.state, "request_id", None)
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        window_start = utcnow() - timedelta(
            seconds=self.settings.auth_rate_limit_window_seconds
        )
        failed_attempts = self.repository.count_recent_failed_login_attempts(
            db,
            identifier=identifier,
            since=window_start.replace(tzinfo=None),
        )

        if failed_attempts >= self.settings.auth_rate_limit_max_attempts:
            self.repository.create_login_audit_event(
                db,
                user_id=None,
                identifier=identifier,
                event_type="login_rate_limited",
                success=False,
                ip_address=ip_address,
                request_id=request_id,
                user_agent=user_agent,
                detail="Too many failed attempts",
            )
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed login attempts. Please try again later.",
            )

        user = self.repository.get_user_by_identifier(db, identifier)

        if not user or not user.is_active or not verify_password(
            payload.password,
            user.password_hash,
        ):
            self.repository.create_login_audit_event(
                db,
                user_id=user.id if user else None,
                identifier=identifier,
                event_type="login_failure",
                success=False,
                ip_address=ip_address,
                request_id=request_id,
                user_agent=user_agent,
                detail="Invalid credentials",
            )
            db.commit()

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token, expires_in = create_access_token(
            subject=str(user.id),
            role=user.role.value,
        )

        self.repository.create_login_audit_event(
            db,
            user_id=user.id,
            identifier=identifier,
            event_type="login_success",
            success=True,
            ip_address=ip_address,
            request_id=request_id,
            user_agent=user_agent,
            detail="Authenticated successfully",
        )
        db.commit()

        return TokenResponse(
            access_token=access_token,
            expires_in=expires_in,
            user=self._build_me_response(user),
        )

    def get_current_user_response(self, user: AdminUser) -> CurrentUserResponse:
        return self._build_me_response(user)

    def forgot_password(
        self,
        db: Session,
        *,
        payload: ForgotPasswordRequest,
        request: Request,
    ) -> ForgotPasswordResponse:
        email = payload.email.strip().lower()
        request_id = getattr(request.state, "request_id", None)
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        generic_response = ForgotPasswordResponse(
            message="If the account exists, a reset token has been generated.",
        )

        user = self.repository.get_user_by_email(db, email)

        if not user or not user.is_active:
            self.repository.create_login_audit_event(
                db,
                user_id=None,
                identifier=email,
                event_type="password_reset_requested",
                success=False,
                ip_address=ip_address,
                request_id=request_id,
                user_agent=user_agent,
                detail="Password reset requested for a non-existing or inactive account",
            )
            db.commit()
            return generic_response

        plain_token = generate_reset_token()
        token_hash = hash_reset_token(plain_token)
        expires_at = utcnow() + timedelta(
            minutes=self.settings.reset_token_expire_minutes
        )

        self.repository.invalidate_active_reset_tokens_for_user(db, user_id=user.id)
        self.repository.create_password_reset_token(
            db,
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at.replace(tzinfo=None),
        )
        self.repository.create_login_audit_event(
            db,
            user_id=user.id,
            identifier=email,
            event_type="password_reset_requested",
            success=True,
            ip_address=ip_address,
            request_id=request_id,
            user_agent=user_agent,
            detail="Password reset token generated",
        )
        db.commit()

        if self.settings.app_env in {"development", "test"}:
            generic_response.reset_token = plain_token

        return generic_response

    def reset_password(
        self,
        db: Session,
        *,
        payload: ResetPasswordRequest,
        request: Request,
    ) -> MessageResponse:
        token_hash = hash_reset_token(payload.token)
        request_id = getattr(request.state, "request_id", None)
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        reset_token = self.repository.get_valid_password_reset_token(
            db,
            token_hash=token_hash,
        )

        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        if normalize_to_utc(reset_token.expires_at) < utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        user = reset_token.user
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or inactive user",
            )

        user.password_hash = get_password_hash(payload.new_password)
        reset_token.used_at = utcnow().replace(tzinfo=None)

        self.repository.create_login_audit_event(
            db,
            user_id=user.id,
            identifier=user.email,
            event_type="password_reset_completed",
            success=True,
            ip_address=ip_address,
            request_id=request_id,
            user_agent=user_agent,
            detail="Password updated successfully",
        )
        db.commit()

        return MessageResponse(
            message="Password updated successfully.",
        )

    def _build_me_response(self, user: AdminUser) -> CurrentUserResponse:
        return CurrentUserResponse.model_validate(user)