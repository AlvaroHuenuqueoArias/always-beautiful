import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("always-beautiful-api")


def http_exception_handler(request: Request, exc: HTTPException):
    """
    Maneja errores HTTP lanzados por el backend.
    """

    logger.warning(
        f"HTTPException | path={request.url.path} | status={exc.status_code} | detail={exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "http_error",
                "message": exc.detail,
                "path": request.url.path,
            }
        },
    )


def generic_exception_handler(request: Request, exc: Exception):
    """
    Maneja errores inesperados del sistema.
    """

    logger.error(
        f"UnhandledException | path={request.url.path} | error={str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "message": "Internal server error",
                "path": request.url.path,
            }
        },
    )