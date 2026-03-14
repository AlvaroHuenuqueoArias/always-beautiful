from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/system",
    tags=["system"]
)


@router.get("/health")
def system_health():
    """
    Health check del sistema completo.
    Usado por monitoreo y orquestadores.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/info")
def system_info():
    """
    Información básica del servicio.
    """
    return {
        "service": "always-beautiful-api",
        "version": "0.1.0",
        "environment": "development"
    }


@router.get("/metrics")
def system_metrics():
    """
    Endpoint inicial para métricas del sistema.
    En el futuro puede integrarse con Prometheus.
    """
    return {
        "uptime": "unknown",
        "requests_total": "not_implemented",
        "errors_total": "not_implemented"
    }