from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.admin.routes import router as admin_router
from app.booking.routes import router as booking_router
from app.cart.routes import router as cart_router
from app.catalog.routes import router as catalog_router
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

configure_logging()

app = FastAPI(
    title="Always Beautiful API",
    version="0.1.0",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seguridad HTTP
app.add_middleware(SecurityHeadersMiddleware)

# Logging y trazabilidad
app.add_middleware(RequestLoggingMiddleware)

# Manejadores globales de errores
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Routers de módulos
app.include_router(shipping_router)
app.include_router(payments_router)
app.include_router(orders_router)
app.include_router(notifications_router)
app.include_router(booking_router)
app.include_router(schedule_router)
app.include_router(observability_router)
app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    return {"status": "ok"}