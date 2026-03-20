from datetime import date, datetime
from typing import Dict, List, Optional

from app.admin.schemas import (
    AdminDashboardKPIs,
    AdminDashboardResponse,
    AdminSummaryResponse,
)
from app.booking.routes import booking_service
from app.booking.schemas import BookingResponse, BookingStatus
from app.catalog.routes import catalog_service
from app.catalog.schemas import CatalogItemResponse
from app.orders.routes import order_service
from app.orders.schemas import OrderResponse


class AdminService:
    def get_dashboard(
        self,
        booking_date: date,
        professional_id: Optional[str] = None,
    ) -> AdminDashboardResponse:
        orders = order_service.list_orders()
        bookings = booking_service.list_bookings()
        catalog_items = catalog_service.list_items()

        daily_bookings = self._filter_bookings_by_date_and_professional(
            bookings=bookings,
            booking_date=booking_date,
            professional_id=professional_id,
        )
        active_catalog_items = self._filter_active_catalog_items(catalog_items)
        recent_orders = self._get_recent_orders(orders, limit=5)

        active_bookings_for_day = [
            booking
            for booking in daily_bookings
            if booking.status == BookingStatus.BOOKED
        ]

        cancelled_bookings_for_day = [
            booking
            for booking in daily_bookings
            if booking.status == BookingStatus.CANCELLED
        ]

        kpis = AdminDashboardKPIs(
            total_orders=len(orders),
            total_bookings=len(bookings),
            total_catalog_items=len(catalog_items),
            total_active_catalog_items=len(active_catalog_items),
            total_bookings_for_day=len(daily_bookings),
            total_active_bookings_for_day=len(active_bookings_for_day),
            total_cancelled_bookings_for_day=len(cancelled_bookings_for_day),
        )

        return AdminDashboardResponse(
            generated_at=datetime.utcnow(),
            booking_date=booking_date,
            professional_id=professional_id,
            kpis=kpis,
            recent_orders=recent_orders,
            daily_bookings=daily_bookings,
            active_catalog_items=active_catalog_items,
            orders_by_status=self._count_orders_by_status(orders),
            bookings_by_status=self._count_bookings_by_status(daily_bookings),
        )

    def get_summary(
        self,
        booking_date: date,
        professional_id: Optional[str] = None,
    ) -> AdminSummaryResponse:
        orders = order_service.list_orders()
        bookings = booking_service.list_bookings()
        catalog_items = catalog_service.list_items()

        daily_bookings = self._filter_bookings_by_date_and_professional(
            bookings=bookings,
            booking_date=booking_date,
            professional_id=professional_id,
        )
        active_catalog_items = self._filter_active_catalog_items(catalog_items)

        return AdminSummaryResponse(
            booking_date=booking_date,
            professional_id=professional_id,
            total_orders=len(orders),
            total_bookings=len(daily_bookings),
            total_catalog_items=len(catalog_items),
            total_active_catalog_items=len(active_catalog_items),
        )

    def _filter_bookings_by_date_and_professional(
        self,
        bookings: List[BookingResponse],
        booking_date: date,
        professional_id: Optional[str] = None,
    ) -> List[BookingResponse]:
        result: List[BookingResponse] = []

        for booking in bookings:
            if booking.start_at.date() != booking_date:
                continue

            if professional_id is not None and booking.professional_id != professional_id:
                continue

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

    def _count_orders_by_status(
        self,
        orders: List[OrderResponse],
    ) -> Dict[str, int]:
        counters: Dict[str, int] = {}

        for order in orders:
            status_name = order.status.value
            counters[status_name] = counters.get(status_name, 0) + 1

        return counters

    def _count_bookings_by_status(
        self,
        bookings: List[BookingResponse],
    ) -> Dict[str, int]:
        counters: Dict[str, int] = {}

        for booking in bookings:
            status_name = booking.status.value
            counters[status_name] = counters.get(status_name, 0) + 1

        return counters