from app.assistant.policies import (
    PROFESSIONAL_COSMETOLOGIST,
    PROFESSIONAL_STYLIST,
)


PROFESSIONALS = [
    {
        "id": "professional-stylist",
        "role": PROFESSIONAL_STYLIST,
        "can_cover": ["styling", "hair"],
    },
    {
        "id": "professional-cosmetologist",
        "role": PROFESSIONAL_COSMETOLOGIST,
        "can_cover": ["cosmetology", "facial", "skincare", "styling", "hair"],
    },
]


def list_professionals() -> list[dict[str, object]]:
    return PROFESSIONALS


def find_professionals_for_service(service_focus: str) -> list[dict[str, object]]:
    normalized_focus = service_focus.lower().strip()

    if not normalized_focus:
        return PROFESSIONALS

    matches = [
        professional
        for professional in PROFESSIONALS
        if normalized_focus in professional["can_cover"]
    ]

    return matches or PROFESSIONALS

