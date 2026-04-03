from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.db.models import AdminRole


class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("identifier")
    @classmethod
    def normalize_identifier(cls, value: str) -> str:
        return value.strip()


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    role: AdminRole
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: CurrentUserResponse


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str
    reset_token: str | None = None


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=16, max_length=255)
    new_password: str = Field(..., min_length=8, max_length=128)


class MessageResponse(BaseModel):
    message: str