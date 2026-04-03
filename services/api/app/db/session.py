from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, or_, select
from sqlalchemy.orm import Session, sessionmaker

from app.auth.security import get_password_hash
from app.core.config import get_settings
from app.db.base import Base
from app.db.models import AdminRole, AdminUser


settings = get_settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    future=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    seed_default_admin_users()


def seed_default_admin_users() -> None:
    default_users = [
        {
            "username": settings.admin_owner_username,
            "email": settings.admin_owner_email,
            "password": settings.admin_owner_password,
            "role": AdminRole.ADMIN_OWNER,
        },
        {
            "username": settings.admin_technical_username,
            "email": settings.admin_technical_email,
            "password": settings.admin_technical_password,
            "role": AdminRole.ADMIN_TECHNICAL,
        },
    ]

    with SessionLocal() as db:
        created_any = False

        for item in default_users:
            if not item["username"] or not item["email"] or not item["password"]:
                continue

            existing_user = db.scalar(
                select(AdminUser).where(
                    or_(
                        AdminUser.username == item["username"],
                        AdminUser.email == item["email"],
                    )
                )
            )

            if existing_user:
                continue

            db.add(
                AdminUser(
                    username=item["username"],
                    email=item["email"],
                    password_hash=get_password_hash(item["password"]),
                    role=item["role"],
                    is_active=True,
                )
            )
            created_any = True

        if created_any:
            db.commit()