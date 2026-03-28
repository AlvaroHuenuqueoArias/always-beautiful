from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.logging_config import configure_logging
from app.observability.state import observability_state


logger = configure_logging()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware de observabilidad que:
    - asigna request_id
    - cuenta requests
    - registra duración y estado final
    """

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        observability_state.increment_requests()
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception(
                "Request failed | request_id=%s | method=%s | path=%s | duration_ms=%.2f",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Request completed | request_id=%s | method=%s | path=%s | status=%s | duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        response.headers["X-Request-ID"] = request_id
        return response