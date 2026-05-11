from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.admin.routes import router as admin_router
from app.assistant.routes import router as assistant_router
from app.auth.routes import router as auth_router
from app.booking.routes import router as booking_router
from app.cart.routes import router as cart_router
from app.catalog.routes import router as catalog_router
from app.core.config import get_settings
from app.db.session import init_db
from app.notifications.routes import router as notifications_router
from app.observability.error_handlers import (
    generic_exception_handler,
    http_exception_handler,
)
from app.observability.logging_config import configure_logging
from app.observability.middleware import RequestLoggingMiddleware
from app.observability.routes import router as observability_router
from app.observability.security_headers import SecurityHeadersMiddleware
from app.orders.routes import router as orders_router
from app.payments.routes import router as payments_router
from app.schedule.routes import router as schedule_router
from app.shipping.routes import router as shipping_router


settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router)
app.include_router(shipping_router)
app.include_router(payments_router)
app.include_router(orders_router)
app.include_router(notifications_router)
app.include_router(booking_router)
app.include_router(schedule_router)
app.include_router(observability_router)
app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(assistant_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    return {"status": "ok"}
