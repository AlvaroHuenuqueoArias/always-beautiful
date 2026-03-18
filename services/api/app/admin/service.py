from datetime import date, datetime
from typing import List

from app.admin.schemas import (
    AdminDashboardKPIs,
    AdminDashboardResponse,
)
from app.booking.routes import booking_service
from app.booking.schemas import BookingResponse, BookingStatus
from app.catalog.routes import catalog_service
from app.catalog.schemas import CatalogItemResponse
from app.orders.routes import order_service
from app.orders.schemas import OrderResponse


class AdminService:
    def get_dashboard(self, booking_date: date) -> AdminDashboardResponse:
        orders = order_service.list_orders()
        bookings = booking_service.list_bookings()
        catalog_items = catalog_service.list_items()

        daily_bookings = self._filter_daily_bookings(bookings, booking_date)
        active_catalog_items = self._filter_active_catalog_items(catalog_items)
        recent_orders = self._get_recent_orders(orders, limit=5)

        kpis = AdminDashboardKPIs(
            total_orders=len(orders),
            total_bookings=len(bookings),
            total_catalog_items=len(catalog_items),
            total_active_catalog_items=len(active_catalog_items),
            total_bookings_for_day=len(daily_bookings),
        )

        return AdminDashboardResponse(
            generated_at=datetime.utcnow(),
            booking_date=booking_date,
            kpis=kpis,
            recent_orders=recent_orders,
            daily_bookings=daily_bookings,
            active_catalog_items=active_catalog_items,
        )

    def _filter_daily_bookings(
        self,
        bookings: List[BookingResponse],
        booking_date: date,
    ) -> List[BookingResponse]:
        result: List[BookingResponse] = []

        for booking in bookings:
            if (
                booking.start_at.date() == booking_date
                and booking.status == BookingStatus.BOOKED
            ):
                result.append(booking)

        return result

    def _filter_active_catalog_items(
        self,
        catalog_items: List[CatalogItemResponse],
    ) -> List[CatalogItemResponse]:
        return [item for item in catalog_items if item.is_active]

    def _get_recent_orders(
        self,
        orders: List[OrderResponse],
        limit: int = 5,
    ) -> List[OrderResponse]:
        return orders[-limit:] if len(orders) > limit else orders