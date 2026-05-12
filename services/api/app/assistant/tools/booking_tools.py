from app.assistant.policies import (
    PROFESSIONAL_COSMETOLOGIST,
    PROFESSIONAL_MARIA_IGNACIA,
    PROFESSIONAL_NADIA_LUISA,
    SERVICE_CATEGORY_COSMETOLOGY,
    SERVICE_CATEGORY_STYLING,
    SERVICE_CATEGORY_UNKNOWN,
    booking_deposit_required_notice,
    booking_deposit_notice,
    booking_safety_notice,
    detect_has_day_signal,
    detect_has_time_signal,
    detect_requested_professional,
    detect_service_category,
    detects_booking_deposit_avoidance,
    get_professional_service_incompatibility,
)
from app.assistant.tools.availability_tools import (
    get_read_only_availability_guidance,
)
from app.assistant.tools.payment_tools import build_deposit_next_action
from app.assistant.tools.professional_tools import find_professionals_for_service


def detect_service_focus(message: str) -> str:
    service_category = detect_service_category(message)

    if service_category in {SERVICE_CATEGORY_STYLING, SERVICE_CATEGORY_COSMETOLOGY}:
        return service_category

    return service_category if service_category != SERVICE_CATEGORY_UNKNOWN else ""


def build_booking_guidance(message: str) -> dict[str, object]:
    if detects_booking_deposit_avoidance(message):
        return {
            "message": (
                f"{booking_deposit_required_notice()} "
                "Puedo orientarte para iniciar una reserva de servicio o "
                f"tratamiento. {booking_deposit_notice()} "
                f"{booking_safety_notice()}"
            ),
            "professionals": [],
            "next_actions": [
                "Elegir servicio o tratamiento desde la web.",
                "Seleccionar profesional disponible: Estilista profesional o Cosmetóloga.",
                build_deposit_next_action(),
                "Esperar confirmación operativa del salón.",
            ],
        }

    incompatibility = get_professional_service_incompatibility(message)

    if incompatibility:
        return {
            "message": str(incompatibility["message"]),
            "professionals": [str(incompatibility["alternative_professional"])],
            "next_actions": list(incompatibility["next_actions"]),
        }

    if detect_has_day_signal(message) or detect_has_time_signal(message):
        availability_guidance = get_read_only_availability_guidance(message)

        return {
            "message": str(availability_guidance["message"]),
            "professionals": [],
            "next_actions": list(availability_guidance["next_actions"]),
        }

    service_focus = detect_service_focus(message)
    requested_professional = detect_requested_professional(message)
    professionals = find_professionals_for_service(service_focus)
    professional_roles = [
        str(professional["role"]) for professional in professionals
    ]

    response = (
        "Puedo orientarte para iniciar una reserva de servicio o tratamiento. "
        f"{booking_deposit_notice()} {booking_safety_notice()}"
    )

    if (
        requested_professional == PROFESSIONAL_MARIA_IGNACIA
        and service_focus == SERVICE_CATEGORY_COSMETOLOGY
    ):
        response = (
            f"{response} María Ignacia puede atender servicios de "
            "cosmetología."
        )

    if (
        requested_professional == PROFESSIONAL_NADIA_LUISA
        and service_focus == SERVICE_CATEGORY_STYLING
    ):
        response = (
            f"{response} Nadia Luisa puede atender servicios de estilismo "
            "profesional."
        )

    if (
        requested_professional == PROFESSIONAL_MARIA_IGNACIA
        and service_focus == SERVICE_CATEGORY_STYLING
    ):
        response = (
            f"{response} María Ignacia también puede cubrir agenda de "
            "estilismo profesional cuando corresponda."
        )

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
