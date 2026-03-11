from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Query, status

# CAMBIO: se elimina el uso del helper externo de availability
from app.booking.repository import BookingRepository
from app.booking.schemas import BookingCreate, BookingResponse
from app.booking.service import BookingService

router = APIRouter(prefix="/bookings", tags=["bookings"])

booking_repository = BookingRepository()
booking_service = BookingService(booking_repository)


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate) -> BookingResponse:
    return booking_service.create_booking(payload)


@router.get("", response_model=List[BookingResponse], status_code=status.HTTP_200_OK)
def list_bookings() -> List[BookingResponse]:
    return booking_service.list_bookings()


@router.get("/{booking_id}", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def get_booking_by_id(booking_id: UUID) -> BookingResponse:
    return booking_service.get_booking_by_id(booking_id)


@router.patch("/{booking_id}/cancel", response_model=BookingResponse, status_code=status.HTTP_200_OK)
def cancel_booking(booking_id: UUID) -> BookingResponse:
    return booking_service.cancel_booking(booking_id)


@router.get("/availability/daily", response_model=List[BookingResponse], status_code=status.HTTP_200_OK)
def get_daily_availability(
    professional_id: str = Query(..., min_length=1),
    booking_date: date = Query(...),
) -> List[BookingResponse]:
    return booking_service.get_daily_availability(professional_id, booking_date)


@router.get("/availability/slots", status_code=status.HTTP_200_OK)
def get_available_slots_route(
    professional_id: str = Query(..., min_length=1),
    booking_date: date = Query(...),
    service_duration: int = Query(..., gt=0),
):
    # CAMBIO: el endpoint ahora usa la lógica oficial del service
    return booking_service.get_available_slots(
        professional_id,
        booking_date,
        service_duration,
    )