from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.shipping.routes import router as shipping_router
from app.payments.routes import router as payments_router
from app.orders.routes import router as orders_router   # ← NUEVO MODULO ORDERS
from app.notifications.routes import router as notifications_router   # ← NUEVO MODULO NOTIFICATIONS
from app.booking.routes import router as booking_router   # ← NUEVO MODULO BOOKING


app = FastAPI(
    title="Always Beautiful API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers de módulos
app.include_router(shipping_router)
app.include_router(payments_router)
app.include_router(orders_router)
app.include_router(notifications_router)
app.include_router(booking_router)


@app.get("/health")
def health():
    return {"status": "ok"}
