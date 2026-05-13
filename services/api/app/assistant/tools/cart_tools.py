from app.assistant.policies import (
    BOOKING_DEPOSIT_PERCENTAGE,
    SERVICE_CATEGORY_COSMETOLOGY,
    SERVICE_CATEGORY_STYLING,
    SERVICE_CATEGORY_TREATMENT,
    SERVICE_CATEGORY_UNKNOWN,
    detect_requested_professional,
    detect_requested_time_label,
    detect_service_category,
)


BOOKING_DEPOSIT_CART_TYPE = "booking_deposit"
BOOKING_DEPOSIT_CART_STATUS = "pending_deposit"
BOOKING_DEPOSIT_CONFIRMATION_STATUS = "not_confirmed"
BOOKING_DEPOSIT_REDIRECT_TARGET = "/cart"

DAY_LABELS = (
    ("lunes", "lunes"),
    ("martes", "martes"),
    ("miércoles", "miércoles"),
    ("miercoles", "miércoles"),
    ("jueves", "jueves"),
    ("viernes", "viernes"),
    ("sábado", "sábado"),
    ("sabado", "sábado"),
    ("domingo", "domingo"),
    ("mañana", "mañana"),
    ("manana", "mañana"),
    ("hoy", "hoy"),
)

DEPOSIT_HANDOFF_PHRASES = (
    "continuar y pagar abono",
    "continuar y pagar el abono",
    "pagar abono",
    "pagar el abono",
    "cancelar abono",
    "cancelar el abono",
)


def build_cart_next_actions() -> list[str]:
    return [
        "Agregar el producto seleccionado al carrito web.",
        "Revisar cantidades antes de continuar.",
        "Finalizar compra solo desde el flujo web autorizado.",
    ]


def detects_deposit_handoff_intent(message: str) -> bool:
    normalized_message = message.lower()

    return any(
        phrase in normalized_message
        for phrase in DEPOSIT_HANDOFF_PHRASES
    )


def build_booking_deposit_cart_payload(message: str) -> dict[str, object] | None:
    if not detects_deposit_handoff_intent(message):
        return None

    service_category = detect_service_category(message)
    professional_label = detect_requested_professional(message)
    requested_day = _detect_requested_day_label(message)
    requested_time = detect_requested_time_label(message)
    service_label = _detect_service_label(message, service_category)

    if (
        service_category == SERVICE_CATEGORY_UNKNOWN
        or professional_label is None
        or requested_day is None
        or requested_time is None
        or service_label is None
    ):
        return None

    return {
        "type": BOOKING_DEPOSIT_CART_TYPE,
        "status": BOOKING_DEPOSIT_CART_STATUS,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
        "service_label": service_label,
        "professional_label": professional_label,
        "requested_day": requested_day,
        "requested_time": requested_time,
        "confirmation_status": BOOKING_DEPOSIT_CONFIRMATION_STATUS,
    }


def _detect_requested_day_label(message: str) -> str | None:
    normalized_message = message.lower()

    for keyword, label in DAY_LABELS:
        if keyword in normalized_message:
            return label

    return None


def _detect_service_label(message: str, service_category: str) -> str | None:
    normalized_message = message.lower()

    if "limpieza facial" in normalized_message:
        return "Limpieza facial"

    if "facial" in normalized_message:
        return "Servicio facial"

    if "peinado" in normalized_message:
        return "Peinado"

    if "corte" in normalized_message:
        return "Corte de cabello"

    if "estilismo" in normalized_message:
        return "Servicio de estilismo"

    if "tratamiento" in normalized_message:
        return "Tratamiento"

    if service_category == SERVICE_CATEGORY_COSMETOLOGY:
        return "Servicio de cosmetología"

    if service_category == SERVICE_CATEGORY_STYLING:
        return "Servicio de estilismo"

    if service_category == SERVICE_CATEGORY_TREATMENT:
        return "Tratamiento"

    if service_category == SERVICE_CATEGORY_UNKNOWN:
        return None

    return None
