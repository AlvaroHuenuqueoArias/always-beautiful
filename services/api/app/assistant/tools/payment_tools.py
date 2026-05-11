from app.assistant.policies import (
    BOOKING_DEPOSIT_PERCENTAGE,
    booking_deposit_notice,
)


def get_booking_deposit_policy() -> dict[str, object]:
    return {
        "requires_deposit": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
        "notice": booking_deposit_notice(),
    }


def build_deposit_next_action() -> str:
    return (
        "Cancelar el "
        f"{BOOKING_DEPOSIT_PERCENTAGE}% del valor del servicio desde la web "
        "para confirmar la hora."
    )

