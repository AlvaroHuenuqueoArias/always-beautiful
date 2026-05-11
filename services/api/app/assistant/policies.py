BOOKING_DEPOSIT_PERCENTAGE = 20

PROFESSIONAL_STYLIST = "Estilista profesional"
PROFESSIONAL_COSMETOLOGIST = "Cosmetóloga"

BOOKING_DEPOSIT_AVOIDANCE_PHRASES = {
    "sin pagar",
    "sin abono",
    "no quiero pagar",
    "sin cancelar",
    "reservar sin pagar",
    "puedo reservar sin pagar",
    "me puedes agendar sin abono",
}


def booking_deposit_notice() -> str:
    return (
        "Para confirmar la hora se debe cancelar el "
        f"{BOOKING_DEPOSIT_PERCENTAGE}% del valor del servicio desde la web."
    )


def booking_safety_notice() -> str:
    return (
        "Puedo orientar la reserva, pero no confirmo horarios, precios ni "
        "disponibilidad real en esta etapa."
    )


def booking_deposit_required_notice() -> str:
    return (
        "No se puede confirmar una reserva sin cancelar el "
        f"{BOOKING_DEPOSIT_PERCENTAGE}% del valor del servicio desde la web."
    )


def detects_booking_deposit_avoidance(message: str) -> bool:
    normalized_message = message.lower()
    return any(
        phrase in normalized_message
        for phrase in BOOKING_DEPOSIT_AVOIDANCE_PHRASES
    )
