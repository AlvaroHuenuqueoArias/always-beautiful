import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.logging_config import configure_logging


logger = configure_logging()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware de observabilidad que registra cada request HTTP.
    """

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        duration_ms = (time.time() - start_time) * 1000

        logger.info(
            f"{request.method} {request.url.path} | "
            f"{response.status_code} | "
            f"{duration_ms:.2f} ms"
        )

        return response