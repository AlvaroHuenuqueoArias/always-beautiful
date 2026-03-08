from datetime import date
from typing import List
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from app.booking.repository import BookingRepository
from app.booking.schemas import (
    BookingCreate,
    BookingResponse,
    BookingStatus,
)


class BookingService:
    def __init__(self, repository: BookingRepository) -> None:
        self.repository = repository

    def create_booking(self, payload: BookingCreate) -> BookingResponse:
        if payload.end_at <= payload.start_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_at must be greater than start_at",
            )

        self._ensure_no_overlap(
            professional_id=payload.professional_id,
            start_at=payload.start_at,
            end_at=payload.end_at,
        )

        booking = BookingResponse(
            id=uuid4(),
            professional_id=payload.professional_id,
            service_name=payload.service_name,
            client_name=payload.client_name,
            client_email=payload.client_email,
            start_at=payload.start_at,
            end_at=payload.end_at,
            status=BookingStatus.BOOKED,
            notes=payload.notes,
        )

        return self.repository.save(booking)

    def list_bookings(self) -> List[BookingResponse]:
        return self.repository.list_all()

    def get_booking_by_id(self, booking_id: UUID) -> BookingResponse:
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        return booking

    def cancel_booking(self, booking_id: UUID) -> BookingResponse:
        booking = self.get_booking_by_id(booking_id)

        updated_booking = booking.model_copy(
            update={"status": BookingStatus.CANCELLED}
        )
        return self.repository.update(updated_booking)

    def get_daily_availability(
        self, professional_id: str, booking_date: date
    ) -> List[BookingResponse]:
        result: List[BookingResponse] = []

        for booking in self.repository.list_all():
            if (
                booking.professional_id == professional_id
                and booking.start_at.date() == booking_date
                and booking.status == BookingStatus.BOOKED
            ):
                result.append(booking)

        return result

    def _ensure_no_overlap(self, professional_id, start_at, end_at) -> None:
        for booking in self.repository.list_all():
            if booking.professional_id != professional_id:
                continue

            if booking.status == BookingStatus.CANCELLED:
                continue

            has_overlap = start_at < booking.end_at and end_at > booking.start_at
            if has_overlap:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Booking overlaps with an existing reservation",
                )