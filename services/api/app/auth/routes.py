from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin_user
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
from app.auth.service import AuthService
from app.db.models import AdminUser
from app.db.session import get_db


router = APIRouter(prefix="/auth", tags=["auth"])

auth_repository = AuthRepository()
auth_service = AuthService(auth_repository)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return auth_service.login(
        db,
        payload=payload,
        request=request,
    )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
)
def me(
    current_user: AdminUser = Depends(require_admin_user),
) -> CurrentUserResponse:
    return auth_service.get_current_user_response(current_user)


@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
    status_code=status.HTTP_200_OK,
)
def forgot_password(
    payload: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> ForgotPasswordResponse:
    return auth_service.forgot_password(
        db,
        payload=payload,
        request=request,
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def reset_password(
    payload: ResetPasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> MessageResponse:
    return auth_service.reset_password(
        db,
        payload=payload,
        request=request,
    )