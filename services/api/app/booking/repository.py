from typing import Dict, List, Optional
from uuid import UUID

from app.booking.schemas import BookingResponse


class BookingRepository:
    def __init__(self) -> None:
        self._bookings: Dict[UUID, BookingResponse] = {}

    def save(self, booking: BookingResponse) -> BookingResponse:
        self._bookings[booking.id] = booking
        return booking

    def get_by_id(self, booking_id: UUID) -> Optional[BookingResponse]:
        return self._bookings.get(booking_id)

    def list_all(self) -> List[BookingResponse]:
        return list(self._bookings.values())

    def update(self, booking: BookingResponse) -> BookingResponse:
        self._bookings[booking.id] = booking
        return booking