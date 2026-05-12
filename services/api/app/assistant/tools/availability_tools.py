from app.assistant.policies import (
    booking_deposit_notice,
    detect_requested_time_label,
)
from app.assistant.state import AssistantFlowStep


MOCK_AVAILABLE_TIMES = {"15:00", "16:00"}
MOCK_UNAVAILABLE_TIMES = {"13:00", "18:30"}
MOCK_WORK_START_TIME = "11:00"
MOCK_WORK_END_TIME = "19:00"


def _time_to_minutes(time_label: str) -> int:
    hour, minute = time_label.split(":", maxsplit=1)
    return int(hour) * 60 + int(minute)


def _is_within_mock_work_window(time_label: str) -> bool:
    requested_minutes = _time_to_minutes(time_label)

    return (
        _time_to_minutes(MOCK_WORK_START_TIME)
        <= requested_minutes
        < _time_to_minutes(MOCK_WORK_END_TIME)
    )


def get_read_only_availability_guidance(message: str) -> dict[str, object]:
    requested_time = detect_requested_time_label(message)

    if requested_time is None:
        return {
            "status": "needs_time",
            "flow_step": AssistantFlowStep.TIME_SELECTION.value,
            "message": "Perfecto. ¿A qué hora prefieres agendar ese día?",
            "next_actions": [
                "Indicar una hora.",
                "Buscar horario disponible.",
                "Cambiar día.",
            ],
        }

    if (
        requested_time in MOCK_UNAVAILABLE_TIMES
        or not _is_within_mock_work_window(requested_time)
    ):
        return {
            "status": "unavailable",
            "flow_step": AssistantFlowStep.TIME_SELECTION.value,
            "message": (
                "Ese horario no aparece disponible en la revisión inicial. "
                "Puedo ayudarte a buscar otro horario tentativo."
            ),
            "next_actions": [
                "Probar 16:00.",
                "Probar 17:00.",
                "Buscar otro día.",
            ],
        }

    return {
        "status": "available",
        "flow_step": AssistantFlowStep.AVAILABILITY_CHECK.value,
        "message": (
            "Ese horario aparece disponible de forma tentativa. "
            f"{booking_deposit_notice()}"
        ),
        "next_actions": [
            "Continuar y pagar abono del 20%.",
            "Buscar otro horario.",
            "Cambiar profesional.",
        ],
    }
