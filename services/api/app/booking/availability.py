from datetime import date

from app.booking.repository import BookingRepository
from app.booking.schemas import BookingStatus
from app.booking.slots import generate_daily_slots


def get_available_slots(
    repository: BookingRepository,
    professional_id: str,
    booking_date: date,
    service_duration: int,
):
    slots = generate_daily_slots(service_duration)

    # CAMBIO: filtrar solo reservas activas del profesional y del día
    active_bookings = [
        booking
        for booking in repository.list_all()
        if (
            booking.professional_id == professional_id
            and booking.status == BookingStatus.BOOKED
            and booking.start_at.date() == booking_date
        )
    ]

    available = []

    for slot in slots:
        is_free = True

        for booking in active_bookings:
            if booking.start_at.time() == slot:
                is_free = False
                break

        if is_free:
            available.append(slot)

    return available