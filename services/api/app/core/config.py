from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


API_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = API_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "always-beautiful-api"
    app_version: str = "0.1.0"
    app_env: str = "development"

    secret_key: str = "change-this-in-local-env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    reset_token_expire_minutes: int = 30

    docs_enabled: bool = True
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    database_url: str = "sqlite:///./always_beautiful.db"

    auth_rate_limit_max_attempts: int = 5
    auth_rate_limit_window_seconds: int = 300

    admin_owner_email: str | None = None
    admin_owner_username: str | None = None
    admin_owner_password: str | None = None

    admin_technical_email: str | None = None
    admin_technical_username: str | None = None
    admin_technical_password: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def docs_url(self) -> str | None:
        return "/docs" if self.docs_enabled else None

    @property
    def redoc_url(self) -> str | None:
        return "/redoc" if self.docs_enabled else None

    @property
    def openapi_url(self) -> str | None:
        return "/openapi.json" if self.docs_enabled else None


@lru_cache
def get_settings() -> Settings:
    return Settings()