import re

from app.assistant.state import AssistantFlowStep


BOOKING_DEPOSIT_PERCENTAGE = 20

PROFESSIONAL_STYLIST = "Estilista profesional"
PROFESSIONAL_COSMETOLOGIST = "Cosmetóloga"

BOOKING_CONVERSION_INTENT_KEYWORDS = {
    "agenda",
    "agendar",
    "cita",
    "hora",
    "reservar",
    "reserva",
}

PRODUCT_FLOW_KEYWORDS = {
    "comprar",
    "compra",
    "producto",
    "carrito",
    "shampoo",
    "crema",
    "serum",
    "mascarilla",
    "recomienda",
    "recomendación",
}

BOOKING_SERVICE_KEYWORDS = {
    "servicio",
    "tratamiento",
    "peinado",
    "corte",
    "facial",
    "estilismo",
}

DAY_KEYWORDS = {
    "lunes",
    "martes",
    "miércoles",
    "miercoles",
    "jueves",
    "viernes",
    "sábado",
    "sabado",
    "domingo",
    "hoy",
    "mañana",
    "manana",
}

TIME_KEYWORDS = {
    "am",
    "pm",
    "a.m.",
    "p.m.",
    "hrs",
}

DEFAULT_BOOKING_FLOW_STEP = AssistantFlowStep.COMPLETED.value

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


def _contains_any_keyword(message: str, keywords: set[str]) -> bool:
    return any(keyword in message for keyword in keywords)


def _contains_time_signal(message: str) -> bool:
    if re.search(r"\b(?:a las|a la)\s+\d{1,2}\b", message):
        return True

    if re.search(r"\b(?:[01]?\d|2[0-3])[:.][0-5]\d\b", message):
        return True

    return bool(re.search(r"\d", message)) and _contains_any_keyword(
        message,
        TIME_KEYWORDS,
    )


def get_booking_conversion_flow_step(message: str) -> str:
    normalized_message = message.lower()

    if _contains_any_keyword(normalized_message, PRODUCT_FLOW_KEYWORDS):
        return AssistantFlowStep.PRODUCT_SELECTION.value

    if detects_booking_deposit_avoidance(normalized_message):
        return AssistantFlowStep.DEPOSIT_CONFIRMATION.value

    has_booking_intent = _contains_any_keyword(
        normalized_message,
        BOOKING_CONVERSION_INTENT_KEYWORDS,
    )
    has_service_signal = _contains_any_keyword(
        normalized_message,
        BOOKING_SERVICE_KEYWORDS,
    )
    has_day_signal = _contains_any_keyword(normalized_message, DAY_KEYWORDS)
    has_time_signal = _contains_time_signal(normalized_message)

    if has_day_signal and not has_time_signal:
        return AssistantFlowStep.TIME_SELECTION.value

    if has_booking_intent and not has_service_signal:
        return AssistantFlowStep.SERVICE_SELECTION.value

    if has_booking_intent and has_service_signal:
        return AssistantFlowStep.PROFESSIONAL_SELECTION.value

    return DEFAULT_BOOKING_FLOW_STEP
