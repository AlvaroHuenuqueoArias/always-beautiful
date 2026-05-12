import re

from app.assistant.state import AssistantFlowStep


BOOKING_DEPOSIT_PERCENTAGE = 20

PROFESSIONAL_STYLIST = "Estilista profesional"
PROFESSIONAL_COSMETOLOGIST = "Cosmetóloga"
PROFESSIONAL_NADIA_LUISA = "Nadia Luisa"
PROFESSIONAL_MARIA_IGNACIA = "María Ignacia"

SERVICE_CATEGORY_STYLING = "styling"
SERVICE_CATEGORY_COSMETOLOGY = "cosmetology"
SERVICE_CATEGORY_TREATMENT = "treatment"
SERVICE_CATEGORY_UNKNOWN = "unknown"

NADIA_LUISA_KEYWORDS = {
    "nadia",
    "nadia luisa",
}

MARIA_IGNACIA_KEYWORDS = {
    "maria",
    "maría",
    "ignacia",
    "maria ignacia",
    "maría ignacia",
}

STYLING_SERVICE_KEYWORDS = {
    "cabello",
    "corte",
    "peinado",
    "brushing",
    "tinte",
    "color",
    "coloración",
    "coloracion",
    "alisado",
    "balayage",
    "estilismo",
    "styling",
}

COSMETOLOGY_SERVICE_KEYWORDS = {
    "cosmetologia",
    "cosmetología",
    "cosmetológica",
    "facial",
    "limpieza",
    "piel",
    "skincare",
    "depilación",
    "depilacion",
    "manicure",
    "pedicure",
    "pestañas",
    "pestanas",
    "maquillaje",
}

TREATMENT_SERVICE_KEYWORDS = {
    "tratamiento",
    "botox",
    "masaje",
}

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


def detect_has_day_signal(message: str) -> bool:
    return _contains_any_keyword(message.lower(), DAY_KEYWORDS)


def detect_has_time_signal(message: str) -> bool:
    return _contains_time_signal(message.lower())


def _normalize_time_label(hour: int, minute: int = 0, period: str = "") -> str:
    normalized_hour = hour
    normalized_period = period.lower().replace(".", "")

    if normalized_period == "pm" and normalized_hour < 12:
        normalized_hour += 12

    if normalized_period == "am" and normalized_hour == 12:
        normalized_hour = 0

    return f"{normalized_hour:02d}:{minute:02d}"


def detect_requested_time_label(message: str) -> str | None:
    normalized_message = message.lower()

    explicit_time_match = re.search(
        r"\b([01]?\d|2[0-3])[:.]([0-5]\d)\b",
        normalized_message,
    )

    if explicit_time_match:
        return _normalize_time_label(
            int(explicit_time_match.group(1)),
            int(explicit_time_match.group(2)),
        )

    relative_time_match = re.search(
        r"\b(?:a las|a la)\s+([01]?\d|2[0-3])\b",
        normalized_message,
    )

    if relative_time_match:
        return _normalize_time_label(int(relative_time_match.group(1)))

    period_time_match = re.search(
        r"\b([1-9]|1[0-2])\s*(a\.?m\.?|p\.?m\.?)\b",
        normalized_message,
    )

    if period_time_match:
        return _normalize_time_label(
            int(period_time_match.group(1)),
            period=period_time_match.group(2),
        )

    hour_label_match = re.search(
        r"\b([01]?\d|2[0-3])\s*(?:hrs?|horas?)\b",
        normalized_message,
    )

    if hour_label_match:
        return _normalize_time_label(int(hour_label_match.group(1)))

    standalone_hour_match = re.search(
        r"\b([01]?\d|2[0-3])\b(?!\s*%)",
        normalized_message,
    )

    if standalone_hour_match:
        return _normalize_time_label(int(standalone_hour_match.group(1)))

    return None


def get_booking_conversion_flow_step(message: str) -> str:
    normalized_message = message.lower()

    if _contains_any_keyword(normalized_message, PRODUCT_FLOW_KEYWORDS):
        return AssistantFlowStep.PRODUCT_SELECTION.value

    if detects_booking_deposit_avoidance(normalized_message):
        return AssistantFlowStep.DEPOSIT_CONFIRMATION.value

    if get_professional_service_incompatibility(normalized_message):
        return AssistantFlowStep.PROFESSIONAL_SELECTION.value

    has_booking_intent = _contains_any_keyword(
        normalized_message,
        BOOKING_CONVERSION_INTENT_KEYWORDS,
    )
    has_service_signal = _contains_any_keyword(
        normalized_message,
        BOOKING_SERVICE_KEYWORDS,
    )
    has_day_signal = detect_has_day_signal(normalized_message)
    has_time_signal = detect_has_time_signal(normalized_message)

    if has_day_signal and not has_time_signal:
        return AssistantFlowStep.TIME_SELECTION.value

    if has_day_signal and has_time_signal:
        return AssistantFlowStep.AVAILABILITY_CHECK.value

    if has_booking_intent and not has_service_signal:
        return AssistantFlowStep.SERVICE_SELECTION.value

    if has_booking_intent and has_service_signal:
        return AssistantFlowStep.PROFESSIONAL_SELECTION.value

    return DEFAULT_BOOKING_FLOW_STEP


def detect_requested_professional(message: str) -> str | None:
    normalized_message = message.lower()
    requested_professionals = []

    if _contains_any_keyword(normalized_message, NADIA_LUISA_KEYWORDS):
        requested_professionals.append(PROFESSIONAL_NADIA_LUISA)

    if _contains_any_keyword(normalized_message, MARIA_IGNACIA_KEYWORDS):
        requested_professionals.append(PROFESSIONAL_MARIA_IGNACIA)

    if len(requested_professionals) == 1:
        return requested_professionals[0]

    return None


def detect_service_category(message: str) -> str:
    normalized_message = message.lower()

    if _contains_any_keyword(normalized_message, COSMETOLOGY_SERVICE_KEYWORDS):
        return SERVICE_CATEGORY_COSMETOLOGY

    if _contains_any_keyword(normalized_message, STYLING_SERVICE_KEYWORDS):
        return SERVICE_CATEGORY_STYLING

    if _contains_any_keyword(normalized_message, TREATMENT_SERVICE_KEYWORDS):
        return SERVICE_CATEGORY_TREATMENT

    return SERVICE_CATEGORY_UNKNOWN


def get_professional_service_incompatibility(
    message: str,
) -> dict[str, object] | None:
    requested_professional = detect_requested_professional(message)
    service_category = detect_service_category(message)

    if (
        requested_professional == PROFESSIONAL_NADIA_LUISA
        and service_category == SERVICE_CATEGORY_COSMETOLOGY
    ):
        return {
            "professional": PROFESSIONAL_NADIA_LUISA,
            "service_category": SERVICE_CATEGORY_COSMETOLOGY,
            "alternative_professional": PROFESSIONAL_MARIA_IGNACIA,
            "message": (
                "Nadia Luisa no realiza servicios de cosmetología. Para ese "
                "servicio puede atenderte María Ignacia."
            ),
            "next_actions": [
                "Continuar con María Ignacia.",
                "Cambiar servicio.",
                "Elegir otra profesional.",
            ],
        }

    return None
