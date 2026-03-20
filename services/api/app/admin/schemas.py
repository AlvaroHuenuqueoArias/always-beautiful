from datetime import date, datetime
from typing import Dict, List, Optional

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
    total_active_bookings_for_day: int
    total_cancelled_bookings_for_day: int


class AdminSummaryResponse(BaseModel):
    booking_date: date
    professional_id: Optional[str] = None
    total_orders: int
    total_bookings: int
    total_catalog_items: int
    total_active_catalog_items: int


class AdminDashboardResponse(BaseModel):
    generated_at: datetime
    booking_date: date
    professional_id: Optional[str] = None
    kpis: AdminDashboardKPIs
    recent_orders: List[OrderResponse]
    daily_bookings: List[BookingResponse]
    active_catalog_items: List[CatalogItemResponse]
    orders_by_status: Dict[str, int]
    bookings_by_status: Dict[str, int]