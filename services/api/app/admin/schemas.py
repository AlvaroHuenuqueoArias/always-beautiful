from datetime import date, datetime
from typing import List

from pydantic import BaseModel

from app.booking.schemas import BookingResponse
from app.catalog.schemas import CatalogItemResponse
from app.orders.schemas import OrderResponse


class AdminDashboardKPIs(BaseModel):
    total_orders: int
    total_bookings: int
    total_catalog_items: int
    total_active_catalog_items: int
    total_bookings_for_day: int


class AdminDashboardResponse(BaseModel):
    generated_at: datetime
    booking_date: date
    kpis: AdminDashboardKPIs
    recent_orders: List[OrderResponse]
    daily_bookings: List[BookingResponse]
    active_catalog_items: List[CatalogItemResponse]