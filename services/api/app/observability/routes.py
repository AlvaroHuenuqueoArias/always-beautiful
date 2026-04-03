from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.auth.dependencies import require_admin_technical, require_admin_user
from app.core.config import get_settings
from app.observability.state import observability_state


settings = get_settings()

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
def system_health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/info", dependencies=[Depends(require_admin_user)])
def system_info():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get("/metrics", dependencies=[Depends(require_admin_technical)])
def system_metrics():
    return observability_state.as_metrics()