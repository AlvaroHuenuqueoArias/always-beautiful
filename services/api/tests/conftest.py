from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

TEST_DB_FILE = Path("test_stage_c.sqlite3")

os.environ["APP_ENV"] = "test"
os.environ["APP_NAME"] = "always-beautiful-api"
os.environ["APP_VERSION"] = "0.1.0"
os.environ["DOCS_ENABLED"] = "true"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-longer-than-32-bytes"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["RESET_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_FILE}"
os.environ["ALLOWED_ORIGINS"] = "http://localhost:5173,http://127.0.0.1:5173"
os.environ["AUTH_RATE_LIMIT_WINDOW_SECONDS"] = "300"
os.environ["AUTH_RATE_LIMIT_MAX_ATTEMPTS"] = "5"

os.environ["ADMIN_OWNER_USERNAME"] = "owner-admin"
os.environ["ADMIN_OWNER_EMAIL"] = "owner@example.com"
os.environ["ADMIN_OWNER_PASSWORD"] = "OwnerPass123!"

os.environ["ADMIN_TECHNICAL_USERNAME"] = "tech-admin"
os.environ["ADMIN_TECHNICAL_EMAIL"] = "tech@example.com"
os.environ["ADMIN_TECHNICAL_PASSWORD"] = "TechPass123!"

# pylint: disable=wrong-import-position
from app.auth.security import create_access_token, get_password_hash
from app.db.base import Base
from app.db.models import AdminRole, AdminUser
from app.db.session import get_db
from app.main import app


test_engine = create_engine(
    os.environ["DATABASE_URL"],
    connect_args={"check_same_thread": False},
    future=True,
)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def seed_admin_users(db: Session) -> None:
    db.add_all(
        [
            AdminUser(
                username=os.environ["ADMIN_OWNER_USERNAME"],
                email=os.environ["ADMIN_OWNER_EMAIL"],
                password_hash=get_password_hash(os.environ["ADMIN_OWNER_PASSWORD"]),
                role=AdminRole.ADMIN_OWNER,
                is_active=True,
            ),
            AdminUser(
                username=os.environ["ADMIN_TECHNICAL_USERNAME"],
                email=os.environ["ADMIN_TECHNICAL_EMAIL"],
                password_hash=get_password_hash(os.environ["ADMIN_TECHNICAL_PASSWORD"]),
                role=AdminRole.ADMIN_TECHNICAL,
                is_active=True,
            ),
        ]
    )
    db.commit()


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    with TestingSessionLocal() as db:
        seed_admin_users(db)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session: Session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def owner_user(db_session: Session) -> AdminUser:
    return db_session.scalar(
        select(AdminUser).where(
            AdminUser.username == os.environ["ADMIN_OWNER_USERNAME"]
        )
    )


@pytest.fixture()
def tech_user(db_session: Session) -> AdminUser:
    return db_session.scalar(
        select(AdminUser).where(
            AdminUser.username == os.environ["ADMIN_TECHNICAL_USERNAME"]
        )
    )


@pytest.fixture()
def owner_token_headers(owner_user: AdminUser) -> dict[str, str]:
    token, _expires_in = create_access_token(
        subject=str(owner_user.id),
        role=owner_user.role.value,
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def tech_token_headers(tech_user: AdminUser) -> dict[str, str]:
    token, _expires_in = create_access_token(
        subject=str(tech_user.id),
        role=tech_user.role.value,
    )
    return {"Authorization": f"Bearer {token}"}