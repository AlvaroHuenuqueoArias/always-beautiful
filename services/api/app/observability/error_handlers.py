from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.observability.state import observability_state


logger = logging.getLogger("always-beautiful-api")


def _build_error_payload(
    request: Request,
    *,
    error_type: str,
    message: str,
    status_code: int,
) -> dict:
    return {
        "error": {
            "type": error_type,
            "message": message,
            "status_code": status_code,
            "path": request.url.path,
            "request_id": getattr(request.state, "request_id", None),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    }


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """
    Maneja errores HTTP controlados del backend.
    """

    observability_state.increment_http_errors()
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        "HTTPException | request_id=%s | path=%s | status=%s | detail=%s",
        request_id,
        request.url.path,
        exc.status_code,
        exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=_build_error_payload(
            request,
            error_type="http_error",
            message=str(exc.detail),
            status_code=exc.status_code,
        ),
    )


async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Maneja errores inesperados del sistema.
    """

    observability_state.increment_unhandled_errors()
    request_id = getattr(request.state, "request_id", None)

    logger.exception(
        "UnhandledException | request_id=%s | path=%s",
        request_id,
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_build_error_payload(
            request,
            error_type="internal_error",
            message="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    )