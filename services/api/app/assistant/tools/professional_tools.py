from app.assistant.policies import (
    PROFESSIONAL_COSMETOLOGIST,
    PROFESSIONAL_MARIA_IGNACIA,
    PROFESSIONAL_NADIA_LUISA,
    PROFESSIONAL_STYLIST,
    SERVICE_CATEGORY_COSMETOLOGY,
    SERVICE_CATEGORY_STYLING,
)


PROFESSIONALS = [
    {
        "id": "nadia-luisa",
        "name": PROFESSIONAL_NADIA_LUISA,
        "role": PROFESSIONAL_STYLIST,
        "can_cover": [
            SERVICE_CATEGORY_STYLING,
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

FEATURED_SERVICES_BY_PROFESSIONAL = {
    PROFESSIONAL_NADIA_LUISA: [
        {
            "label": "Corte profesional",
            "service_label": "Corte profesional",
        },
        {
            "label": "Brushing profesional",
            "service_label": "Brushing profesional",
        },
        {
            "label": "Peinado social",
            "service_label": "Peinado social",
        },
        {
            "label": "Tratamiento capilar",
            "service_label": "Tratamiento capilar",
        },
        {
            "label": "Coloración / raíz",
            "service_label": "Coloración / raíz",
        },
    ],
    PROFESSIONAL_MARIA_IGNACIA: [
        {
            "label": "Limpieza facial",
            "service_label": "Limpieza facial",
        },
        {
            "label": "Perfilado de cejas",
            "service_label": "Perfilado de cejas",
        },
        {
            "label": "Laminado de cejas",
            "service_label": "Laminado de cejas",
        },
        {
            "label": "Hidratación facial",
            "service_label": "Hidratación facial",
        },
        {
            "label": "Maquillaje",
            "service_label": "Maquillaje",
        },
        {
            "label": "Peinados femeninos",
            "service_label": "Peinados femeninos",
        },
        {
            "label": "Brushing",
            "service_label": "Brushing",
        },
        {
            "label": "Tratamiento capilar",
            "service_label": "Tratamiento capilar",
        },
    ],
}


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


def get_featured_services_for_professional(
    professional_label: str,
) -> list[dict[str, str]]:
    return FEATURED_SERVICES_BY_PROFESSIONAL.get(professional_label, [])


def get_primary_featured_services_for_professional(
    professional_label: str,
) -> list[dict[str, str]]:
    featured_services = get_featured_services_for_professional(professional_label)

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return featured_services

    return featured_services


def get_secondary_featured_services_for_professional(
    professional_label: str,
) -> list[dict[str, str]]:
    featured_services = get_featured_services_for_professional(professional_label)

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return featured_services[5:]

    return []
