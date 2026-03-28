from __future__ import annotations

import os
from datetime import datetime, timezone

from fastapi import APIRouter

from app.observability.state import observability_state


SERVICE_NAME = os.getenv("APP_NAME", "always-beautiful-api")
SERVICE_VERSION = os.getenv("APP_VERSION", "0.1.0")
SERVICE_ENVIRONMENT = os.getenv("APP_ENV", "development")

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
def system_health():
    """
    Health check del sistema completo.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/info")
def system_info():
    """
    Información básica del servicio.
    """
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "environment": SERVICE_ENVIRONMENT,
    }


@router.get("/metrics")
def system_metrics():
    """
    Métricas básicas en memoria del sistema.
    """
    return observability_state.as_metrics()