from app.assistant.policies import (
    PROFESSIONAL_COSMETOLOGIST,
    PROFESSIONAL_MARIA_IGNACIA,
    PROFESSIONAL_NADIA_LUISA,
    PROFESSIONAL_STYLIST,
    SERVICE_CATEGORY_COSMETOLOGY,
    SERVICE_CATEGORY_STYLING,
    SERVICE_CATEGORY_TREATMENT,
)


PROFESSIONALS = [
    {
        "id": "nadia-luisa",
        "name": PROFESSIONAL_NADIA_LUISA,
        "role": PROFESSIONAL_STYLIST,
        "can_cover": [
            SERVICE_CATEGORY_STYLING,
            SERVICE_CATEGORY_TREATMENT,
            "hair",
        ],
        "blocked_categories": [SERVICE_CATEGORY_COSMETOLOGY],
    },
    {
        "id": "maria-ignacia",
        "name": PROFESSIONAL_MARIA_IGNACIA,
        "role": PROFESSIONAL_COSMETOLOGIST,
        "can_cover": [
            SERVICE_CATEGORY_COSMETOLOGY,
            SERVICE_CATEGORY_STYLING,
            "facial",
            "skincare",
            "hair",
        ],
        "blocked_categories": [],
    },
]


def list_professionals() -> list[dict[str, object]]:
    return PROFESSIONALS


def find_professional_by_name(name: str) -> dict[str, object] | None:
    normalized_name = name.lower().strip()

    for professional in PROFESSIONALS:
        if str(professional["name"]).lower() == normalized_name:
            return professional

    return None


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
