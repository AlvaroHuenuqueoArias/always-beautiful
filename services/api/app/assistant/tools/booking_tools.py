from app.assistant.policies import (
    PROFESSIONAL_COSMETOLOGIST,
    booking_deposit_required_notice,
    booking_deposit_notice,
    booking_safety_notice,
    detects_booking_deposit_avoidance,
)
from app.assistant.tools.payment_tools import build_deposit_next_action
from app.assistant.tools.professional_tools import find_professionals_for_service


STYLING_KEYWORDS = {
    "cabello",
    "corte",
    "peinado",
    "tinte",
    "color",
    "alisado",
    "estilismo",
    "styling",
}

COSMETOLOGY_KEYWORDS = {
    "facial",
    "limpieza",
    "piel",
    "cosmetologia",
    "cosmetológica",
    "tratamiento",
    "skincare",
}


def detect_service_focus(message: str) -> str:
    normalized_message = message.lower()

    if any(keyword in normalized_message for keyword in STYLING_KEYWORDS):
        return "styling"

    if any(keyword in normalized_message for keyword in COSMETOLOGY_KEYWORDS):
        return "cosmetology"

    return ""


def build_booking_guidance(message: str) -> dict[str, object]:
    service_focus = detect_service_focus(message)
    professionals = find_professionals_for_service(service_focus)
    professional_roles = [
        str(professional["role"]) for professional in professionals
    ]

    response = (
        "Puedo orientarte para iniciar una reserva de servicio o tratamiento. "
        f"{booking_deposit_notice()} {booking_safety_notice()}"
    )

    if detects_booking_deposit_avoidance(message):
        response = f"{booking_deposit_required_notice()} {response}"

    if PROFESSIONAL_COSMETOLOGIST in professional_roles:
        response = (
            f"{response} La cosmetóloga también puede cubrir agenda para "
            "servicios de estilismo profesional cuando corresponda."
        )

    return {
        "message": response,
        "professionals": professional_roles,
        "next_actions": [
            "Elegir servicio o tratamiento desde la web.",
            "Seleccionar profesional disponible: Estilista profesional o Cosmetóloga.",
            build_deposit_next_action(),
            "Esperar confirmación operativa del salón.",
        ],
    }
