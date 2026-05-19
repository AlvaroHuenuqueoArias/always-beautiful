from app.assistant.policies import (
    BOOKING_DEPOSIT_PERCENTAGE,
    PROFESSIONAL_COSMETOLOGIST,
    PROFESSIONAL_MARIA_IGNACIA,
    PROFESSIONAL_NADIA_LUISA,
    PROFESSIONAL_STYLIST,
    SERVICE_CATEGORY_COSMETOLOGY,
    SERVICE_CATEGORY_NAILS,
    SERVICE_CATEGORY_STYLING,
    SERVICE_CATEGORY_TREATMENT,
    SERVICE_CATEGORY_UNKNOWN,
    detect_requested_professional,
    detect_requested_time_label,
    detect_service_category,
    detects_deposit_payment_intent,
    normalize_message_text,
)


BOOKING_DEPOSIT_CART_TYPE = "booking_deposit"
BOOKING_DEPOSIT_CART_STATUS = "pending_deposit"
BOOKING_DEPOSIT_CONFIRMATION_STATUS = "not_confirmed"
BOOKING_DEPOSIT_PAYMENT_STATUS = "deposit_pending"
BOOKING_SCHEDULE_PENDING_CONFIRMATION_STATUS = "pending_confirmation"
BOOKING_SCHEDULE_PENDING_SELECTION_STATUS = "pending_selection"
BOOKING_AMOUNT_PENDING_FINAL_PRICE_STATUS = "pending_final_price"
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


def build_cart_next_actions() -> list[str]:
    return [
        "Agregar el producto seleccionado al carrito web.",
        "Revisar cantidades antes de continuar.",
        "Finalizar compra solo desde el flujo web autorizado.",
    ]


def detects_deposit_handoff_intent(message: str) -> bool:
    return detects_deposit_payment_intent(message)


def build_booking_deposit_cart_payload(
    message: str,
    context: dict[str, object] | None = None,
) -> dict[str, object] | None:
    if not detects_deposit_handoff_intent(message):
        return None

    context = context or {}
    existing_cart_payload = context.get("cart_payload")

    if (
        isinstance(existing_cart_payload, dict)
        and isinstance(existing_cart_payload.get("items"), list)
        and existing_cart_payload["items"]
    ):
        return existing_cart_payload

    service_category = detect_service_category(message)
    professional_label = detect_requested_professional(message) or _read_context_string(
        context,
        "selected_professional",
    )
    professional_id = _read_context_string(
        context,
        "professional_id",
    ) or _professional_to_payload_id(professional_label)
    professional_role = _read_context_string(
        context,
        "professional_role",
    ) or _professional_role_for_label(professional_label)
    requested_day = detect_requested_day_label(message) or _read_context_string(
        context,
        "requested_day",
    )
    requested_time = detect_requested_time_label(message) or _read_context_string(
        context,
        "requested_time",
    )
    service_label = detect_booking_service_label(message) or _read_context_string(
        context,
        "selected_service",
    )

    if (
        service_category == SERVICE_CATEGORY_UNKNOWN
        and _read_context_string(context, "selected_service") is None
    ):
        return None

    if professional_label is None or service_label is None:
        return None

    schedule_status = (
        BOOKING_SCHEDULE_PENDING_CONFIRMATION_STATUS
        if requested_day and requested_time
        else BOOKING_SCHEDULE_PENDING_SELECTION_STATUS
    )
    cart_item = build_booking_deposit_cart_item(
        service_label=service_label,
        professional_label=professional_label,
        professional_id=professional_id,
        professional_role=professional_role,
    )

    return {
        "type": BOOKING_DEPOSIT_CART_TYPE,
        "status": BOOKING_DEPOSIT_CART_STATUS,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
        "remaining_percentage": 100 - BOOKING_DEPOSIT_PERCENTAGE,
        "amount_status": BOOKING_AMOUNT_PENDING_FINAL_PRICE_STATUS,
        "service_label": service_label,
        "professional_label": professional_label,
        "selected_service": service_label,
        "selected_professional": professional_label,
        "professional_id": professional_id,
        "professional_role": professional_role,
        "requested_day": requested_day,
        "requested_time": requested_time,
        "schedule_status": schedule_status,
        "items": [cart_item],
        "total_items": 1,
        "cart_count": 1,
        "confirmation_status": BOOKING_DEPOSIT_CONFIRMATION_STATUS,
        "payment_status": BOOKING_DEPOSIT_PAYMENT_STATUS,
    }


def build_booking_deposit_cart_item(
    service_label: str,
    professional_label: str,
    professional_id: str | None,
    professional_role: str | None,
) -> dict[str, object]:
    return {
        "professional": professional_label,
        "professional_id": professional_id,
        "professional_role": professional_role,
        "service_label": service_label,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
        "remaining_percentage": 100 - BOOKING_DEPOSIT_PERCENTAGE,
        "amount_status": BOOKING_AMOUNT_PENDING_FINAL_PRICE_STATUS,
    }


def build_booking_deposit_multi_service_cart_payload(
    context: dict[str, object],
    service_labels: list[str],
) -> dict[str, object] | None:
    professional_label = _read_context_string(context, "selected_professional")
    professional_id = _read_context_string(
        context,
        "professional_id",
    ) or _professional_to_payload_id(professional_label)
    professional_role = _read_context_string(
        context,
        "professional_role",
    ) or _professional_role_for_label(professional_label)
    requested_day = _read_context_string(context, "requested_day")
    requested_time = _read_context_string(context, "requested_time")
    deduped_service_labels = [
        service_label
        for index, service_label in enumerate(service_labels)
        if service_label and service_label not in service_labels[:index]
    ]

    if not professional_label or not deduped_service_labels:
        return None

    schedule_status = (
        BOOKING_SCHEDULE_PENDING_CONFIRMATION_STATUS
        if requested_day and requested_time
        else BOOKING_SCHEDULE_PENDING_SELECTION_STATUS
    )
    selected_service = deduped_service_labels[-1]
    items = [
        build_booking_deposit_cart_item(
            service_label=service_label,
            professional_label=professional_label,
            professional_id=professional_id,
            professional_role=professional_role,
        )
        for service_label in deduped_service_labels
    ]

    return {
        "type": BOOKING_DEPOSIT_CART_TYPE,
        "status": BOOKING_DEPOSIT_CART_STATUS,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
        "remaining_percentage": 100 - BOOKING_DEPOSIT_PERCENTAGE,
        "amount_status": BOOKING_AMOUNT_PENDING_FINAL_PRICE_STATUS,
        "service_label": selected_service,
        "professional_label": professional_label,
        "selected_service": selected_service,
        "selected_professional": professional_label,
        "professional_id": professional_id,
        "professional_role": professional_role,
        "requested_day": requested_day,
        "requested_time": requested_time,
        "schedule_status": schedule_status,
        "items": items,
        "total_items": len(items),
        "cart_count": len(items),
        "confirmation_status": BOOKING_DEPOSIT_CONFIRMATION_STATUS,
        "payment_status": BOOKING_DEPOSIT_PAYMENT_STATUS,
    }


def detect_requested_day_label(message: str) -> str | None:
    normalized_message = normalize_message_text(message)

    for keyword, label in DAY_LABELS:
        if normalize_message_text(keyword) in normalized_message:
            return label

    return None


def _read_context_string(
    context: dict[str, object],
    key: str,
) -> str | None:
    value = context.get(key)

    if isinstance(value, str) and value.strip():
        return value.strip()

    return None


def _professional_to_payload_id(professional_label: str | None) -> str | None:
    if professional_label == PROFESSIONAL_NADIA_LUISA:
        return "nadia_luisa"

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return "maria_ignacia"

    return None


def _professional_role_for_label(professional_label: str | None) -> str | None:
    if professional_label == PROFESSIONAL_NADIA_LUISA:
        return PROFESSIONAL_STYLIST

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return PROFESSIONAL_COSMETOLOGIST

    return None


def detect_booking_service_label(message: str) -> str | None:
    service_category = detect_service_category(message)
    normalized_message = normalize_message_text(message)

    if "limpieza facial" in normalized_message:
        return "Limpieza facial"

    if "manicure" in normalized_message:
        return "Manicure tradicional"

    if "esmaltado permanente" in normalized_message:
        return "Esmaltado permanente"

    if "soft gel" in normalized_message:
        return "Soft gel"

    if "diseno de unas" in normalized_message:
        return "Diseño de uñas"

    if "retiro de esmaltado" in normalized_message:
        return "Retiro de esmaltado"

    if "diagnostico facial" in normalized_message:
        return "Diagnóstico facial"

    if "hidratacion facial" in normalized_message:
        return "Hidratación facial"

    if (
        "tratamiento facial" in normalized_message
        or "facial hidratante" in normalized_message
    ):
        return "Tratamiento facial hidratante"

    if "facial" in normalized_message:
        return "Servicio facial"

    if "peinados femeninos" in normalized_message:
        return "Peinados femeninos"

    if "peinado social" in normalized_message or "peinado" in normalized_message:
        if "maria" in normalized_message or "ignacia" in normalized_message:
            return "Peinados femeninos"

        return "Peinado social"

    if "brushing profesional" in normalized_message:
        return "Brushing profesional"

    if "brushing" in normalized_message or "ondas" in normalized_message:
        return "Brushing"

    if "coloracion" in normalized_message or "raiz" in normalized_message:
        return "Coloración / raíz"

    if "corte" in normalized_message:
        return "Corte profesional"

    if "estilismo" in normalized_message:
        return "Servicio de estilismo"

    if "tratamiento" in normalized_message:
        if "capilar" in normalized_message:
            return "Tratamiento capilar"

        if "facial" in normalized_message:
            return "Tratamiento facial hidratante"

        return "Tratamiento"

    if "perfilado" in normalized_message:
        return "Perfilado de cejas"

    if "laminado" in normalized_message:
        return "Laminado de cejas"

    if "depilacion facial" in normalized_message:
        return "Depilación facial"

    if "maquillaje" in normalized_message:
        return "Maquillaje"

    if "preparacion para evento" in normalized_message:
        return "Preparación para evento"

    if "asesoria express" in normalized_message:
        return "Asesoría express de belleza"

    if service_category == SERVICE_CATEGORY_COSMETOLOGY:
        return "Servicio de cosmetología"

    if service_category == SERVICE_CATEGORY_NAILS:
        return "Servicio de uñas"

    if service_category == SERVICE_CATEGORY_STYLING:
        return "Servicio de estilismo"

    if service_category == SERVICE_CATEGORY_TREATMENT:
        return "Tratamiento"

    if service_category == SERVICE_CATEGORY_UNKNOWN:
        return None

    return None
