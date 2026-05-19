from app.assistant.policies import (
    BOOKING_DEPOSIT_PERCENTAGE,
    PROFESSIONAL_COSMETOLOGIST,
    PROFESSIONAL_MARIA_IGNACIA,
    PROFESSIONAL_NADIA_LUISA,
    PROFESSIONAL_STYLIST,
    SERVICE_CATEGORY_COSMETOLOGY,
    SERVICE_CATEGORY_UNKNOWN,
    booking_deposit_required_notice,
    booking_safety_notice,
    detect_has_day_signal,
    detect_has_time_signal,
    detect_requested_professional,
    detect_requested_time_label,
    detect_service_category,
    detects_all_services_intent,
    detects_booking_deposit_avoidance,
    detects_booking_intent,
    normalize_message_text,
)
from app.assistant.state import AssistantFlowStep
from app.assistant.tools.availability_tools import (
    get_read_only_availability_guidance,
)
from app.assistant.tools.cart_tools import (
    BOOKING_DEPOSIT_REDIRECT_TARGET,
    build_booking_deposit_cart_payload,
    build_booking_deposit_multi_service_cart_payload,
    detect_booking_service_label,
    detect_requested_day_label,
    detects_deposit_handoff_intent,
)
from app.assistant.tools.professional_tools import (
    find_professionals_for_service,
    get_featured_services_for_professional,
    get_primary_featured_services_for_professional,
    get_secondary_featured_services_for_professional,
)


BOOKING_PENDING_NOTICE = (
    "La hora queda pendiente hasta confirmación del salón y abono web."
)
BOOKING_DEPOSIT_TERMS_NOTICE = (
    "Al continuar, aceptas los términos y condiciones, la política de "
    "privacidad y las condiciones de reserva de Always Beautiful. El abono "
    "corresponde al 20% y la hora queda pendiente hasta confirmación "
    "operativa. El saldo restante del 80% deberá pagarse según las "
    "condiciones informadas por el salón. El comprobante y las instrucciones "
    "de pago del saldo restante serán enviados al correo registrado."
)
BOOKING_SUPPORT_ACTIONS = [BOOKING_PENDING_NOTICE]
VALID_QUICK_ACTION_TYPES = {"reply", "navigate", "cart_handoff"}
PROFESSIONAL_SERVICE_TARGETS = {
    PROFESSIONAL_NADIA_LUISA: "/services?professional=nadia_luisa",
    PROFESSIONAL_MARIA_IGNACIA: "/services?professional=maria_ignacia",
}
PROFESSIONAL_BOOKING_TARGETS = {
    PROFESSIONAL_NADIA_LUISA: "/booking?professional=nadia_luisa",
    PROFESSIONAL_MARIA_IGNACIA: "/booking?professional=maria_ignacia",
}
NADIA_QUICK_SCHEDULES = (
    ("Miércoles 10:00", "miércoles", "10:00"),
    ("Miércoles 12:00", "miércoles", "12:00"),
    ("Jueves 11:00", "jueves", "11:00"),
    ("Viernes 15:00", "viernes", "15:00"),
    ("Sábado 10:30", "sábado", "10:30"),
)
MARIA_WEEKLY_AVAILABLE_SCHEDULES = (
    ("Lunes 10:00", "lunes", "10:00"),
    ("Lunes 12:30", "lunes", "12:30"),
    ("Martes 11:00", "martes", "11:00"),
    ("Martes 15:30", "martes", "15:30"),
    ("Miércoles 10:00", "miércoles", "10:00"),
    ("Jueves 16:00", "jueves", "16:00"),
    ("Viernes 12:00", "viernes", "12:00"),
    ("Sábado 10:30", "sábado", "10:30"),
)


def detect_service_focus(message: str) -> str:
    service_category = detect_service_category(message)

    return service_category if service_category != SERVICE_CATEGORY_UNKNOWN else ""


def build_booking_guidance(
    message: str,
    context: dict[str, object] | None = None,
) -> dict[str, object]:
    booking_context = build_booking_context(message, context)
    selected_professional = read_context_string(
        booking_context,
        "selected_professional",
    )
    primary_service = read_primary_service_label(booking_context)
    detected_service = detect_booking_service_label(message)

    if detects_assistant_restart_intent(message, context):
        return build_assistant_restart_guidance()

    if detects_cart_redirect_intent(message, context) or detects_cart_redirect_intent(
        message,
        booking_context,
    ):
        return build_cart_redirect_final_guidance(booking_context)

    if detects_add_additional_service_to_cart_intent(
        message,
        context,
    ) or detects_add_additional_service_to_cart_intent(message, booking_context):
        return build_add_additional_service_to_cart_guidance(booking_context)

    if detects_discard_additional_service_intent(
        message,
        context,
    ) or detects_discard_additional_service_intent(message, booking_context):
        return build_discard_additional_service_guidance(booking_context)

    if detects_primary_service_payment_intent(message, context):
        return build_primary_service_payment_guidance(booking_context)

    if (
        selected_professional == PROFESSIONAL_MARIA_IGNACIA
        and is_selecting_additional_service_mode(booking_context)
        and primary_service
        and detected_service
        and detected_service != primary_service
    ):
        return build_multi_service_selection_guidance(booking_context)

    if detects_add_previous_service_to_cart_intent(
        message,
        context,
    ) or detects_add_previous_service_to_cart_intent(message, booking_context):
        return build_add_previous_service_to_cart_guidance(booking_context)

    if detects_discard_previous_service_intent(
        message,
        context,
    ) or detects_discard_previous_service_intent(message, booking_context):
        return build_discard_previous_service_guidance(booking_context)

    if detects_new_service_payment_intent(message, context):
        return build_new_service_payment_guidance(booking_context)

    if detects_change_service_intent(message, context):
        service_change_context = build_service_change_context(booking_context)
        selected_professional = read_context_string(
            service_change_context,
            "selected_professional",
        )
        previous_service = read_previous_service_label(context)

        if selected_professional:
            return build_guidance_response(
                message=build_change_service_message(
                    selected_professional,
                    previous_service,
                ),
                flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
                context=service_change_context,
                quick_replies=build_service_change_quick_replies(
                    selected_professional,
                    service_change_context,
                ),
            )

    selected_professional = read_context_string(
        booking_context,
        "selected_professional",
    )
    selected_service = read_context_string(booking_context, "selected_service")
    requested_day = read_context_string(booking_context, "requested_day")
    requested_time = read_context_string(booking_context, "requested_time")

    if (
        selected_professional
        and selected_service
        and requested_day
        and requested_time
        and read_context_bool(booking_context, "service_change_mode")
    ):
        return build_service_change_abono_guidance(booking_context)

    if detects_booking_deposit_avoidance(message):
        return build_guidance_response(
            message=(
                f"{booking_deposit_required_notice()} "
                f"{booking_safety_notice()}"
            ),
            flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
            context=booking_context,
            quick_replies=build_booking_start_quick_replies(booking_context),
        )

    incompatibility = get_contextual_incompatibility(booking_context)

    if incompatibility:
        blocked_context = {
            **booking_context,
            "flow_step": AssistantFlowStep.PROFESSIONAL_SELECTION.value,
            "availability_status": "blocked",
        }

        return build_guidance_response(
            message=str(incompatibility["message"]),
            flow_step=AssistantFlowStep.PROFESSIONAL_SELECTION.value,
            context=blocked_context,
            next_actions=[
                "Revisamos que el servicio calce con la profesional antes de avanzar."
            ],
            quick_replies=build_professional_switch_quick_replies(
                blocked_context
            ),
        )

    if detects_deposit_handoff_intent(message):
        cart_payload = build_booking_deposit_cart_payload(message, booking_context)

        if cart_payload is None:
            missing_context = {
                **booking_context,
                "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
                "availability_status": "missing_data",
            }

            return build_guidance_response(
                message=(
                    "Te llevaré a reservas para completar servicio y "
                    "profesional antes de preparar el abono."
                ),
                flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
                context=missing_context,
                quick_replies=[build_missing_handoff_quick_reply(missing_context)],
            )

        handoff_context = {
            **booking_context,
            "flow_step": AssistantFlowStep.AVAILABILITY_CHECK.value,
            "availability_status": "available",
            "cart_payload": cart_payload,
        }

        return build_guidance_response(
            message=(
                "Ya tengo los datos principales para preparar el abono. "
                "Puedes revisarlo en el carrito."
            ),
            flow_step=AssistantFlowStep.AVAILABILITY_CHECK.value,
            context=handoff_context,
            next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
            redirect_target=BOOKING_DEPOSIT_REDIRECT_TARGET,
            cart_payload=cart_payload,
            quick_replies=[build_cart_handoff_quick_reply(handoff_context)],
        )

    if has_multi_service_selection(booking_context):
        return build_multi_service_selection_guidance(booking_context)

    if selected_service and selected_professional and not (
        detect_has_day_signal(message) or detect_has_time_signal(message)
    ):
        return build_service_selection_deposit_guidance(booking_context)

    if detects_maria_more_services_intent(message):
        maria_context = {
            **booking_context,
            "selected_professional": PROFESSIONAL_MARIA_IGNACIA,
            "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
        }

        return build_guidance_response(
            message=(
                "También puedes elegir uno de estos servicios destacados "
                "con María Ignacia."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context=maria_context,
            quick_replies=build_featured_service_quick_replies(
                PROFESSIONAL_MARIA_IGNACIA,
                maria_context,
                service_group="secondary",
            ),
        )

    if detects_professional_services_navigation(message, context, booking_context):
        professional_label = read_context_string(
            booking_context,
            "selected_professional",
        )

        if professional_label:
            professional_context = {
                **booking_context,
                "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
            }

            return build_guidance_response(
                message=build_professional_services_navigation_message(
                    professional_label
                ),
                flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
                context=professional_context,
                quick_replies=build_featured_service_quick_replies(
                    professional_label,
                    professional_context,
                ),
            )

    if detects_all_services_intent(message):
        services_context = {
            **booking_context,
            "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
        }

        return build_guidance_response(
            message=(
                "De las dos profesionales que atienden en el salón de "
                "belleza, ¿qué servicios deseas revisar?"
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context=services_context,
            quick_replies=build_services_catalog_quick_replies(services_context),
        )

    if wants_booking_start(message, booking_context):
        start_context = {
            **booking_context,
            "flow_step": AssistantFlowStep.PROFESSIONAL_SELECTION.value,
        }

        return build_guidance_response(
            message=(
                "Perfecto. Te ayudo a avanzar con la reserva. Primero elige "
                "con qué profesional deseas atenderte."
            ),
            flow_step=AssistantFlowStep.PROFESSIONAL_SELECTION.value,
            context=start_context,
            quick_replies=build_booking_start_quick_replies(start_context),
        )

    if is_professional_selection_only(message, booking_context):
        professional_context = {
            **booking_context,
            "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
        }

        return build_guidance_response(
            message=build_professional_services_message(selected_professional),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context=professional_context,
            quick_replies=build_featured_service_quick_replies(
                selected_professional,
                professional_context,
            ),
        )

    if selected_service and selected_professional and requested_day and requested_time:
        availability_guidance = get_read_only_availability_guidance(
            build_context_message(booking_context)
        )

        if is_nadia_quick_schedule(booking_context):
            availability_guidance = {
                "status": "available",
                "flow_step": AssistantFlowStep.AVAILABILITY_CHECK.value,
                "message": "Horario rápido disponible de forma tentativa.",
            }

        availability_status = str(availability_guidance.get("status", "unknown"))
        availability_context = {
            **booking_context,
            "flow_step": str(availability_guidance["flow_step"]),
            "availability_status": availability_status,
        }
        cart_payload = None

        if availability_status == "available":
            cart_payload = build_booking_deposit_cart_payload(
                "pagar abono",
                availability_context,
            )
            availability_context["cart_payload"] = cart_payload

            return build_guidance_response(
                message=(
                    "Ese horario aparece disponible de forma tentativa. "
                    "Ya tengo los datos principales para preparar el abono."
                ),
                flow_step=str(availability_guidance["flow_step"]),
                context=availability_context,
                next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
                cart_payload=cart_payload,
                quick_replies=build_availability_quick_replies(
                    availability_context,
                    cart_payload,
                ),
            )

        return build_guidance_response(
            message=str(availability_guidance["message"]),
            flow_step=str(availability_guidance["flow_step"]),
            context=availability_context,
            quick_replies=build_time_selection_quick_replies(availability_context),
        )

    if selected_service and not selected_professional:
        professional_context = {
            **booking_context,
            "flow_step": AssistantFlowStep.PROFESSIONAL_SELECTION.value,
        }

        return build_guidance_response(
            message=(
                "Perfecto. Te ayudo a avanzar con la reserva. Primero elige "
                "con qué profesional deseas atenderte."
            ),
            flow_step=AssistantFlowStep.PROFESSIONAL_SELECTION.value,
            context=professional_context,
            quick_replies=build_booking_start_quick_replies(professional_context),
        )

    if selected_professional and not selected_service:
        professional_context = {
            **booking_context,
            "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
        }

        return build_guidance_response(
            message=build_professional_services_message(selected_professional),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context=professional_context,
            quick_replies=build_featured_service_quick_replies(
                selected_professional,
                professional_context,
            ),
        )

    return build_guidance_response(
        message=(
            "Puedo ayudarte a reservar una hora. Elige una profesional o "
            "revisa todos los servicios disponibles."
        ),
        flow_step=AssistantFlowStep.PROFESSIONAL_SELECTION.value,
        context=booking_context,
        quick_replies=build_booking_start_quick_replies(booking_context),
    )


def build_booking_context(
    message: str,
    context: dict[str, object] | None = None,
) -> dict[str, object]:
    current_context = dict(context or {})
    nested_context = current_context.pop("context", None)

    if isinstance(nested_context, dict):
        current_context = {**nested_context, **current_context}

    professional_from_payload = normalize_professional_id(
        read_context_string(current_context, "professional")
    )
    professional_from_context = normalize_professional_id(
        read_context_string(current_context, "selected_professional")
    )
    detected_professional = detect_requested_professional(message)

    selected_professional = (
        detected_professional
        or professional_from_payload
        or professional_from_context
    )

    detected_service = detect_booking_service_label(message)
    service_from_context = read_context_string(
        current_context,
        "service_label",
    ) or read_context_string(current_context, "selected_service")
    primary_service_from_context = read_context_string(
        current_context,
        "primary_service",
    )
    additional_service_candidate_from_context = read_context_string(
        current_context,
        "additional_service_candidate",
    )
    preserves_active_service = (
        detects_add_previous_service_to_cart_intent(message, current_context)
        or detects_discard_previous_service_intent(message, current_context)
        or detects_add_additional_service_to_cart_intent(message, current_context)
        or detects_discard_additional_service_intent(message, current_context)
        or detects_primary_service_payment_intent(message, current_context)
    )
    primary_service = primary_service_from_context or service_from_context
    additional_service_candidate = additional_service_candidate_from_context

    if (
        selected_professional == PROFESSIONAL_MARIA_IGNACIA
        and primary_service
        and detected_service
        and detected_service != primary_service
        and not preserves_active_service
        and not detects_change_service_intent(message, current_context)
    ):
        additional_service_candidate = detected_service

    selected_service = (
        primary_service
        if primary_service
        else (
            service_from_context
            if preserves_active_service and service_from_context
            else detected_service or service_from_context
        )
    )
    requested_day = (
        detect_requested_day_label(message)
        or read_context_string(current_context, "requested_day")
    )
    requested_time = (
        detect_requested_time_label(message)
        or read_context_string(current_context, "requested_time")
    )
    cart_payload = current_context.get("cart_payload")

    booking_context: dict[str, object] = {
        "intent": "booking",
        "deposit_required": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
    }

    if selected_professional:
        booking_context["selected_professional"] = selected_professional
        booking_context["professional_id"] = professional_to_payload_id(
            selected_professional
        )

        professional_role = professional_role_for_label(selected_professional)

        if professional_role:
            booking_context["professional_role"] = professional_role

    if selected_service:
        booking_context["selected_service"] = selected_service

    if primary_service:
        booking_context["primary_service"] = primary_service

    if additional_service_candidate:
        booking_context["additional_service_candidate"] = additional_service_candidate

    if requested_day:
        booking_context["requested_day"] = requested_day

    if requested_time:
        booking_context["requested_time"] = requested_time

    if isinstance(current_context.get("service_change_mode"), bool):
        booking_context["service_change_mode"] = bool(
            current_context["service_change_mode"]
        )

    service_selection_mode = current_context.get("service_selection_mode")

    if isinstance(service_selection_mode, str) and service_selection_mode.strip():
        booking_context["service_selection_mode"] = service_selection_mode.strip()
    elif isinstance(service_selection_mode, bool):
        booking_context["service_selection_mode"] = bool(service_selection_mode)

    if isinstance(current_context.get("multi_service_decision_mode"), bool):
        booking_context["multi_service_decision_mode"] = bool(
            current_context["multi_service_decision_mode"]
        )

    cart_items = read_cart_item_service_labels(current_context)

    if cart_items:
        booking_context["cart_items"] = cart_items
        booking_context["cart_count"] = len(cart_items)
    elif (
        isinstance(current_context.get("cart_count"), int)
        and not isinstance(current_context.get("cart_count"), bool)
    ):
        booking_context["cart_count"] = int(current_context["cart_count"])

    previous_service = read_context_string(current_context, "previous_service")

    if previous_service:
        booking_context["previous_service"] = previous_service

    if isinstance(cart_payload, dict):
        booking_context["cart_payload"] = cart_payload

    return booking_context


def build_guidance_response(
    message: str,
    flow_step: str,
    context: dict[str, object],
    next_actions: list[str] | None = None,
    quick_replies: list[dict[str, object]] | None = None,
    redirect_target: str | None = None,
    cart_payload: dict[str, object] | None = None,
) -> dict[str, object]:
    response_context = {
        **context,
        "flow_step": flow_step,
        "deposit_required": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
    }

    if cart_payload:
        response_context["cart_payload"] = cart_payload

    return {
        "message": message,
        "professionals": [],
        "next_actions": BOOKING_SUPPORT_ACTIONS if next_actions is None else next_actions,
        "quick_replies": quick_replies or [],
        "redirect_target": redirect_target,
        "cart_payload": cart_payload,
        "context": response_context,
        "flow_step": flow_step,
    }


def build_quick_reply(
    label: str,
    message: str,
    action_type: str,
    target: str | None = None,
    payload: dict[str, object] | None = None,
    context: dict[str, object] | None = None,
) -> dict[str, object]:
    normalized_action_type = (
        action_type if action_type in VALID_QUICK_ACTION_TYPES else "reply"
    )
    quick_payload = dict(payload or {})

    if context:
        quick_payload["context"] = context

    return {
        "label": label,
        "message": message,
        "action_type": normalized_action_type,
        "target": target,
        "payload": quick_payload or None,
    }


def build_all_services_quick_reply(
    context: dict[str, object] | None = None,
) -> dict[str, object]:
    return build_quick_reply(
        label="Ver todos los servicios",
        message="Quiero ver todos los servicios disponibles para reservar",
        action_type="navigate",
        target="/services",
        payload={"reason": "full_services_catalog"},
        context=context,
    )


def build_professional_services_quick_reply(
    professional_label: str,
    context: dict[str, object],
) -> dict[str, object]:
    label = f"Ver todos los servicios de {professional_short_name(professional_label)}"

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        label = "Ver todos los servicios de María Ignacia"

    return build_quick_reply(
        label=label,
        message=f"Quiero ver todos los servicios de {professional_label}",
        action_type="navigate",
        target=PROFESSIONAL_SERVICE_TARGETS.get(professional_label, "/services"),
        payload={
            "reason": "professional_services_catalog",
            "professional": professional_to_payload_id(professional_label),
        },
        context=context,
    )


def build_services_catalog_quick_replies(
    context: dict[str, object],
) -> list[dict[str, object]]:
    nadia_context = {
        **context,
        "selected_professional": PROFESSIONAL_NADIA_LUISA,
        "professional_id": "nadia_luisa",
        "professional_role": PROFESSIONAL_STYLIST,
    }
    maria_context = {
        **context,
        "selected_professional": PROFESSIONAL_MARIA_IGNACIA,
        "professional_id": "maria_ignacia",
    }

    return [
        build_quick_reply(
            label="Nadia Luisa",
            message="Quiero ver servicios de Nadia Luisa",
            action_type="navigate",
            target=PROFESSIONAL_SERVICE_TARGETS[PROFESSIONAL_NADIA_LUISA],
            payload={
                "reason": "professional_services_catalog",
                "professional": "nadia_luisa",
            },
            context=nadia_context,
        ),
        build_quick_reply(
            label="Maria Ignacia",
            message="Quiero ver servicios de María Ignacia",
            action_type="navigate",
            target=PROFESSIONAL_SERVICE_TARGETS[PROFESSIONAL_MARIA_IGNACIA],
            payload={
                "reason": "professional_services_catalog",
                "professional": "maria_ignacia",
            },
            context=maria_context,
        ),
        build_restart_quick_reply(),
    ]


def build_booking_start_quick_replies(
    context: dict[str, object] | None = None,
) -> list[dict[str, object]]:
    return [
        build_quick_reply(
            label="Nadia Luisa",
            message="Quiero atenderme con Nadia Luisa",
            action_type="reply",
            payload={"professional": "nadia_luisa"},
            context=context,
        ),
        build_quick_reply(
            label="María Ignacia",
            message="Quiero atenderme con María Ignacia",
            action_type="reply",
            payload={"professional": "maria_ignacia"},
            context=context,
        ),
    ]


def build_featured_service_quick_replies(
    professional_label: str | None,
    context: dict[str, object],
    service_group: str = "primary",
) -> list[dict[str, object]]:
    if not professional_label:
        return build_booking_start_quick_replies(context)

    quick_replies = []
    services = get_featured_services_for_professional(professional_label)
    professional_context = {
        **context,
        "selected_professional": professional_label,
        "professional_id": professional_to_payload_id(professional_label),
    }
    professional_role = professional_role_for_label(professional_label)

    if professional_role:
        professional_context["professional_role"] = professional_role

    if service_group == "secondary":
        services = get_secondary_featured_services_for_professional(
            professional_label
        )
    elif service_group == "primary":
        services = get_primary_featured_services_for_professional(
            professional_label
        )

    for service in services:
        service_label = service["service_label"]
        primary_service = read_primary_service_label(professional_context)
        service_context = {
            **professional_context,
            "selected_service": service_label,
            "flow_step": AssistantFlowStep.TIME_SELECTION.value,
        }

        if professional_label == PROFESSIONAL_MARIA_IGNACIA and primary_service:
            service_context = {
                **service_context,
                "selected_service": primary_service,
                "primary_service": primary_service,
                "additional_service_candidate": service_label,
                "service_selection_mode": "selecting_additional_service",
            }

        quick_replies.append(
            build_quick_reply(
                label=service["label"],
                message=f"Quiero reservar {service_label} con {professional_label}",
                action_type="reply",
                payload={
                    "professional": professional_to_payload_id(professional_label),
                    "service_label": service_label,
                },
                context=service_context,
            )
        )

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        quick_replies.append(
            build_professional_services_quick_reply(
                professional_label,
                professional_context,
            )
        )
        quick_replies.append(build_restart_quick_reply())
        return quick_replies

    if professional_label == PROFESSIONAL_NADIA_LUISA:
        quick_replies.append(
            build_nadia_agenda_quick_reply(
                professional_context,
                include_service=False,
            )
        )
        return quick_replies

    quick_replies.append(
        build_booking_draft_quick_reply(
            label="Agendar ahora",
            message=f"Quiero agendar con {professional_label} desde reservas",
            context=professional_context,
            reason="booking_with_professional",
            target=PROFESSIONAL_BOOKING_TARGETS.get(professional_label, "/booking"),
        )
    )
    quick_replies.append(
        build_professional_services_quick_reply(
            professional_label,
            professional_context,
        )
    )
    return quick_replies


def build_maria_more_services_quick_reply(
    context: dict[str, object],
) -> dict[str, object]:
    maria_context = {
        **context,
        "selected_professional": PROFESSIONAL_MARIA_IGNACIA,
    }

    return build_quick_reply(
        label="Ver más servicios de María",
        message="Quiero ver más servicios de María Ignacia",
        action_type="reply",
        payload={"reason": "maria_more_services"},
        context=maria_context,
    )


def build_nadia_agenda_quick_reply(
    context: dict[str, object],
    include_service: bool,
) -> dict[str, object]:
    agenda_context = {
        **context,
        "intent": "booking",
        "selected_professional": PROFESSIONAL_NADIA_LUISA,
        "professional_id": "nadia_luisa",
        "professional_role": PROFESSIONAL_STYLIST,
        "flow_step": "professional_profile",
        "deposit_required": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
    }

    if not include_service:
        agenda_context.pop("selected_service", None)

    return build_quick_reply(
        label="Ver toda la agenda de Nadia",
        message="Quiero ver toda la agenda de Nadia Luisa en reservas",
        action_type="navigate",
        target=PROFESSIONAL_BOOKING_TARGETS[PROFESSIONAL_NADIA_LUISA],
        payload={"reason": "nadia_full_agenda"},
        context=agenda_context,
    )


def build_maria_agenda_quick_reply(
    context: dict[str, object],
    include_service: bool,
) -> dict[str, object]:
    agenda_context = {
        **context,
        "intent": "booking",
        "selected_professional": PROFESSIONAL_MARIA_IGNACIA,
        "professional_id": "maria_ignacia",
        "professional_role": PROFESSIONAL_COSMETOLOGIST,
        "flow_step": "professional_profile",
        "deposit_required": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
    }

    if not include_service:
        agenda_context.pop("selected_service", None)

    return build_quick_reply(
        label="Ver agenda completa de María",
        message="Quiero ver agenda completa de María Ignacia en reservas",
        action_type="navigate",
        target=PROFESSIONAL_BOOKING_TARGETS[PROFESSIONAL_MARIA_IGNACIA],
        payload={"reason": "maria_full_agenda"},
        context=agenda_context,
    )


def build_booking_draft_quick_reply(
    label: str,
    message: str,
    context: dict[str, object],
    reason: str,
    target: str = "/booking",
) -> dict[str, object]:
    return build_quick_reply(
        label=label,
        message=message,
        action_type="navigate",
        target=target,
        payload={"reason": reason},
        context=context,
    )


def build_professional_switch_quick_replies(
    context: dict[str, object],
) -> list[dict[str, object]]:
    maria_context = {
        **context,
        "selected_professional": PROFESSIONAL_MARIA_IGNACIA,
        "professional_id": professional_to_payload_id(PROFESSIONAL_MARIA_IGNACIA),
    }
    maria_role = professional_role_for_label(PROFESSIONAL_MARIA_IGNACIA)

    if maria_role:
        maria_context["professional_role"] = maria_role

    return [
        build_quick_reply(
            label="Continuar con María",
            message="Quiero continuar con María Ignacia",
            action_type="reply",
            payload={"professional": "maria_ignacia"},
            context=maria_context,
        ),
        build_quick_reply(
            label="Cambiar servicio",
            message="Quiero cambiar servicio",
            action_type="reply",
            payload={
                "reason": "change_service",
                "previous_service": read_context_string(
                    context,
                    "selected_service",
                ),
            },
            context={
                key: value
                for key, value in context.items()
                if key
                not in {
                    "selected_service",
                    "availability_status",
                    "cart_payload",
                }
            },
        ),
        build_all_services_quick_reply(context),
    ]


def build_service_change_quick_replies(
    professional_label: str,
    context: dict[str, object],
) -> list[dict[str, object]]:
    professional_context = {
        **context,
        "selected_professional": professional_label,
        "professional_id": professional_to_payload_id(professional_label),
        "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
    }
    professional_role = professional_role_for_label(professional_label)

    if professional_role:
        professional_context["professional_role"] = professional_role

    quick_replies = []

    for service in get_primary_featured_services_for_professional(professional_label):
        service_label = service["service_label"]
        primary_service = read_primary_service_label(professional_context)
        service_context = {
            **professional_context,
            "selected_service": service_label,
            "flow_step": AssistantFlowStep.TIME_SELECTION.value,
        }

        if professional_label == PROFESSIONAL_MARIA_IGNACIA and primary_service:
            service_context = {
                **service_context,
                "selected_service": primary_service,
                "primary_service": primary_service,
                "additional_service_candidate": service_label,
                "service_selection_mode": "selecting_additional_service",
            }

        quick_replies.append(
            build_quick_reply(
                label=service["label"],
                message=f"Quiero reservar {service_label} con {professional_label}",
                action_type="reply",
                payload={
                    "professional": professional_to_payload_id(professional_label),
                    "service_label": service_label,
                },
                context=service_context,
            )
        )

    quick_replies.append(
        build_professional_services_quick_reply(
            professional_label,
            professional_context,
        )
    )
    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        quick_replies.append(build_restart_quick_reply())

    return quick_replies


def build_time_selection_quick_replies(
    context: dict[str, object],
) -> list[dict[str, object]]:
    service_label = read_context_string(context, "selected_service") or "este servicio"
    professional_label = read_context_string(context, "selected_professional")

    if professional_label == PROFESSIONAL_NADIA_LUISA:
        return build_nadia_time_selection_quick_replies(context, service_label)

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return build_maria_time_selection_quick_replies(context, service_label)

    professional_fragment = (
        f" con {professional_label}" if professional_label else ""
    )

    return [
        build_booking_draft_quick_reply(
            label="Elegir horario",
            message=f"Quiero elegir horario para {service_label} en reservas",
            context=context,
            reason="choose_booking_time",
            target=PROFESSIONAL_BOOKING_TARGETS.get(professional_label, "/booking"),
        ),
        build_datetime_quick_reply(
            "Miércoles 15:00",
            "miércoles",
            "15:00",
            service_label,
            professional_fragment,
            context,
        ),
        build_datetime_quick_reply(
            "Miércoles 16:00",
            "miércoles",
            "16:00",
            service_label,
            professional_fragment,
            context,
        ),
        build_quick_reply(
            label="Buscar otro horario",
            message=f"Quiero revisar la agenda completa para {service_label}",
            action_type="navigate",
            target=PROFESSIONAL_BOOKING_TARGETS.get(professional_label, "/booking"),
            payload={"reason": "change_time"},
            context=context,
        ),
        build_quick_reply(
            label="Cambiar profesional",
            message="Quiero cambiar profesional",
            action_type="reply",
            payload={"reason": "change_professional"},
            context={
                key: value
                for key, value in context.items()
                if key != "selected_professional"
            },
        ),
    ]


def build_nadia_time_selection_quick_replies(
    context: dict[str, object],
    service_label: str,
) -> list[dict[str, object]]:
    nadia_context = {
        **context,
        "intent": "booking",
        "selected_professional": PROFESSIONAL_NADIA_LUISA,
        "professional_id": "nadia_luisa",
        "professional_role": PROFESSIONAL_STYLIST,
        "selected_service": service_label,
        "flow_step": AssistantFlowStep.TIME_SELECTION.value,
        "deposit_required": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
    }
    quick_replies = [
        build_datetime_quick_reply(
            label,
            requested_day,
            requested_time,
            service_label,
            " con Nadia Luisa",
            nadia_context,
        )
        for label, requested_day, requested_time in NADIA_QUICK_SCHEDULES
    ]

    quick_replies.append(
        build_nadia_agenda_quick_reply(nadia_context, include_service=True)
    )
    return quick_replies


def build_maria_time_selection_quick_replies(
    context: dict[str, object],
    service_label: str,
) -> list[dict[str, object]]:
    maria_context = {
        **context,
        "intent": "booking",
        "selected_professional": PROFESSIONAL_MARIA_IGNACIA,
        "professional_id": "maria_ignacia",
        "professional_role": PROFESSIONAL_COSMETOLOGIST,
        "selected_service": service_label,
        "flow_step": AssistantFlowStep.TIME_SELECTION.value,
        "deposit_required": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
    }
    quick_replies = [
        build_datetime_quick_reply(
            label,
            requested_day,
            requested_time,
            service_label,
            " con María Ignacia",
            maria_context,
        )
        for label, requested_day, requested_time in MARIA_WEEKLY_AVAILABLE_SCHEDULES
    ]

    quick_replies.append(
        build_maria_agenda_quick_reply(maria_context, include_service=True)
    )
    return quick_replies


def build_datetime_quick_reply(
    label: str,
    requested_day: str,
    requested_time: str,
    service_label: str,
    professional_fragment: str,
    context: dict[str, object],
) -> dict[str, object]:
    datetime_context = {
        **context,
        "requested_day": requested_day,
        "requested_time": requested_time,
        "flow_step": AssistantFlowStep.AVAILABILITY_CHECK.value,
    }

    return build_quick_reply(
        label=label,
        message=(
            f"Quiero reservar {service_label}{professional_fragment} "
            f"el {requested_day} a las {requested_time}"
        ),
        action_type="reply",
        payload={
            "requested_day": requested_day,
            "requested_time": requested_time,
        },
        context=datetime_context,
    )


def build_availability_quick_replies(
    context: dict[str, object],
    cart_payload: dict[str, object] | None,
) -> list[dict[str, object]]:
    quick_replies: list[dict[str, object]] = []
    selected_professional = read_context_string(context, "selected_professional")

    if is_complete_booking_deposit_cart_payload(cart_payload):
        handoff_context = {**context, "cart_payload": cart_payload}
        quick_replies.append(
            build_quick_reply(
                label="Abonar 20% del servicio",
                message="Quiero ir al carrito para pagar el abono del 20%",
                action_type="cart_handoff",
                target="/cart",
                payload={
                    "reason": "booking_deposit_handoff",
                    "cart_payload": cart_payload,
                },
                context=handoff_context,
            )
        )

    quick_replies.extend(
        [
            (
                build_nadia_agenda_quick_reply(context, include_service=True)
                if selected_professional == PROFESSIONAL_NADIA_LUISA
                else build_quick_reply(
                    label="Buscar otro horario",
                    message="Quiero revisar otros horarios en reservas",
                    action_type="navigate",
                    target=PROFESSIONAL_BOOKING_TARGETS.get(
                        selected_professional,
                        "/booking",
                    ),
                    payload={"reason": "change_time"},
                    context=context,
                )
            ),
            build_quick_reply(
                label="Cambiar servicio",
                message="Quiero cambiar servicio",
                action_type="reply",
                payload={
                    "reason": "change_service",
                    "previous_service": read_context_string(
                        context,
                        "selected_service",
                    ),
                },
                context={
                    key: value
                    for key, value in context.items()
                    if key
                    not in {
                        "selected_service",
                        "availability_status",
                        "cart_payload",
                    }
                },
            ),
        ]
    )

    return quick_replies


def build_cart_handoff_quick_reply(context: dict[str, object]) -> dict[str, object]:
    cart_payload = context.get("cart_payload")

    if not is_complete_booking_deposit_cart_payload(cart_payload):
        return build_missing_handoff_quick_reply(context)

    return build_quick_reply(
        label="Abonar 20% del servicio",
        message="Quiero ir al carrito para pagar el abono del 20%",
        action_type="cart_handoff",
        target="/cart",
        payload={
            "reason": "booking_deposit_handoff",
            "cart_payload": cart_payload,
        },
        context=context,
    )


def build_cart_navigation_quick_reply(
    context: dict[str, object] | None = None,
) -> dict[str, object]:
    return build_quick_reply(
        label="Ir a Carrito de compras",
        message="Ir a Carrito de compras",
        action_type="navigate",
        target="/cart",
        payload={"reason": "open_cart"},
        context=context,
    )


def build_cart_redirect_final_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    cart_items = read_cart_item_service_labels(context)
    cart_payload = context.get("cart_payload")
    if not cart_items and isinstance(cart_payload, dict):
        raw_items = cart_payload.get("items")

        if isinstance(raw_items, list):
            for item in raw_items:
                if not isinstance(item, dict):
                    continue

                service_label = read_context_string(item, "service_label")
                if service_label and service_label not in cart_items:
                    cart_items.append(service_label)

    if not isinstance(cart_payload, dict) and cart_items:
        cart_payload = build_booking_deposit_multi_service_cart_payload(
            context,
            cart_items,
        )

    cart_count = len(cart_items)

    redirect_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "additional_service_candidate",
                "multi_service_decision_mode",
                "service_selection_mode",
                "availability_status",
            }
        },
        "checkout_ready": True,
        "conversation_locked": True,
        "cart_redirected": True,
        "cart_items": cart_items,
        "cart_count": cart_count,
    }

    if cart_payload:
        redirect_context["cart_payload"] = cart_payload

    return build_guidance_response(
        message=(
            "Perfecto. Te llevé al carrito para revisar el detalle de tu "
            "selección. La hora quedará pendiente hasta confirmación del "
            "salón. Importante: si presionas Volver a iniciar, se "
            "reiniciará el chat y se eliminarán las selecciones actuales "
            "del carrito. Tendrás que comenzar el proceso nuevamente."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=redirect_context,
        next_actions=[],
        cart_payload=cart_payload if isinstance(cart_payload, dict) else None,
        quick_replies=[build_restart_quick_reply()],
    )


def build_abono_quick_reply(context: dict[str, object]) -> dict[str, object]:
    cart_payload = context.get("cart_payload")

    if not is_complete_booking_deposit_cart_payload(cart_payload):
        return build_missing_handoff_quick_reply(context)

    return build_quick_reply(
        label="Abonar 20% del servicio",
        message="Quiero ir al carrito para pagar el abono del 20%",
        action_type="cart_handoff",
        target="/cart",
        payload={
            "reason": "booking_deposit_handoff",
            "cart_payload": cart_payload,
        },
        context=context,
    )


def build_other_services_quick_reply(
    professional_label: str,
    context: dict[str, object],
) -> dict[str, object]:
    selected_service = read_context_string(context, "selected_service")
    primary_service = read_primary_service_label(context) or selected_service
    label = f"Ver todos los servicios de {professional_short_name(professional_label)}"

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        label = "Ver todos los servicios de María Ignacia"

    return build_quick_reply(
        label=label,
        message=label,
        action_type="reply",
        payload={
            "reason": "change_service",
            "previous_service": selected_service,
            "primary_service": primary_service,
        },
        context={
            key: value
            for key, value in context.items()
            if key
            not in {
                "availability_status",
                "cart_payload",
            }
        }
        | {
            "previous_service": selected_service,
            "primary_service": primary_service,
            "service_change_mode": True,
            "service_selection_mode": (
                "selecting_additional_service"
                if professional_label == PROFESSIONAL_MARIA_IGNACIA
                and primary_service
                else True
            ),
        },
    )


def build_add_previous_service_to_cart_quick_reply(
    previous_service: str,
    context: dict[str, object],
) -> dict[str, object]:
    return build_quick_reply(
        label=f"Agregar {previous_service} al carrito",
        message=f"Agregar {previous_service} al carrito",
        action_type="reply",
        payload={"reason": "add_previous_service_to_cart"},
        context={
            **context,
            "service_selection_mode": True,
            "multi_service_decision_mode": True,
        },
    )


def build_discard_previous_service_quick_reply(
    previous_service: str,
    context: dict[str, object],
) -> dict[str, object]:
    return build_quick_reply(
        label=f"Descartar {previous_service}",
        message=f"Descartar {previous_service}",
        action_type="reply",
        payload={"reason": "discard_previous_service"},
        context={
            **context,
            "service_selection_mode": True,
            "multi_service_decision_mode": True,
        },
    )


def build_selected_service_abono_quick_reply(
    service_label: str,
    context: dict[str, object],
    *,
    action_type: str = "cart_handoff",
    target: str | None = BOOKING_DEPOSIT_REDIRECT_TARGET,
    reason: str = "pay_selected_service",
) -> dict[str, object]:
    cart_payload = build_booking_deposit_multi_service_cart_payload(
        context,
        build_selected_service_payment_labels(context, service_label),
    )
    payment_context = {
        **context,
        "cart_payload": cart_payload,
        "service_selection_mode": True,
    }

    return build_quick_reply(
        label=f"Abonar 20% de {service_label}",
        message=f"Abonar 20% de {service_label}",
        action_type=action_type,
        target=(
            target
            if is_complete_booking_deposit_cart_payload(cart_payload)
            else None
        ),
        payload={
            "reason": reason,
            "cart_payload": cart_payload,
        },
        context=payment_context,
    )


def build_primary_service_abono_quick_reply(
    primary_service: str,
    context: dict[str, object],
    *,
    action_type: str = "cart_handoff",
    target: str | None = BOOKING_DEPOSIT_REDIRECT_TARGET,
    reason: str = "pay_primary_service",
) -> dict[str, object]:
    service_labels = build_primary_service_payment_labels(context, primary_service)
    cart_payload = build_booking_deposit_multi_service_cart_payload(
        context,
        service_labels,
    )
    payment_context = {
        **context,
        "selected_service": primary_service,
        "primary_service": primary_service,
        "cart_payload": cart_payload,
        "service_selection_mode": True,
    }

    return build_quick_reply(
        label=f"Abonar 20% de {primary_service}",
        message=f"Abonar 20% de {primary_service}",
        action_type=action_type,
        target=(
            target
            if is_complete_booking_deposit_cart_payload(cart_payload)
            else None
        ),
        payload={
            "reason": reason,
            "cart_payload": cart_payload,
        },
        context=payment_context,
    )


def build_add_additional_service_to_cart_quick_reply(
    additional_service: str,
    context: dict[str, object],
) -> dict[str, object]:
    return build_quick_reply(
        label=f"Abonar 20% de {additional_service}",
        message=f"Abonar 20% de {additional_service}",
        action_type="reply",
        payload={"reason": "add_additional_service_to_cart"},
        context={
            **context,
            "additional_service_candidate": additional_service,
            "service_selection_mode": True,
            "multi_service_decision_mode": True,
        },
    )


def build_discard_additional_service_quick_reply(
    additional_service: str,
    context: dict[str, object],
) -> dict[str, object]:
    return build_quick_reply(
        label=f"Descartar {additional_service}",
        message=f"Descartar {additional_service}",
        action_type="reply",
        payload={"reason": "discard_additional_service"},
        context={
            **context,
            "additional_service_candidate": additional_service,
            "service_selection_mode": True,
            "multi_service_decision_mode": True,
        },
    )


def build_add_more_services_quick_reply(
    context: dict[str, object],
) -> dict[str, object]:
    primary_service = read_primary_service_label(context)
    add_more_context = {
        key: value
        for key, value in context.items()
        if key
        not in {
            "additional_service_candidate",
            "multi_service_decision_mode",
            "availability_status",
            "cart_payload",
        }
    }

    if primary_service:
        add_more_context["primary_service"] = primary_service
        add_more_context["selected_service"] = primary_service

    add_more_context["service_selection_mode"] = (
        "selecting_additional_service" if primary_service else True
    )

    return build_quick_reply(
        label="Agregar más servicios",
        message="Agregar más servicios",
        action_type="reply",
        payload={"reason": "change_service"},
        context=add_more_context,
    )


def build_multi_service_checkout_ready_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    primary_service = read_primary_service_label(context)
    cart_items = read_cart_item_service_labels(context)
    if primary_service and primary_service not in cart_items:
        cart_items.append(primary_service)

    cart_payload = build_booking_deposit_multi_service_cart_payload(
        {
            **context,
            "selected_service": primary_service,
            "primary_service": primary_service,
            "checkout_ready": True,
            "conversation_locked": True,
        },
        cart_items,
    )

    if cart_payload is None:
        return build_guidance_response(
            message=(
                "Para preparar el cierre del carrito necesito definir primero "
                "los servicios seleccionados."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context={
                key: value
                for key, value in context.items()
                if key not in {"cart_payload", "availability_status"}
            },
            quick_replies=[build_missing_handoff_quick_reply(context)],
        )

    def format_service_list(service_labels: list[str]) -> str:
        if not service_labels:
            return ""

        if len(service_labels) == 1:
            return service_labels[0]

        if len(service_labels) == 2:
            return f"{service_labels[0]} y {service_labels[1]}"

        return ", ".join(service_labels[:-1]) + f" y {service_labels[-1]}"

    checkout_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "additional_service_candidate",
                "multi_service_decision_mode",
                "previous_service",
                "service_selection_mode",
                "availability_status",
            }
        },
        "selected_service": primary_service,
        "primary_service": primary_service,
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "cart_payload": cart_payload,
        "cart_items": cart_items,
        "cart_count": len(cart_items),
        "checkout_ready": True,
        "conversation_locked": True,
    }

    return build_cart_redirect_final_guidance(checkout_context)


def build_service_selection_deposit_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    selected_professional = read_context_string(context, "selected_professional")
    selected_service = read_context_string(context, "selected_service")
    cart_payload = build_booking_deposit_cart_payload("pagar abono", context)
    deposit_context = {
        **context,
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "availability_status": "pending_schedule_selection",
        "cart_payload": cart_payload,
    }

    if cart_payload is None:
        return build_guidance_response(
            message=(
                "Para preparar el abono necesito definir primero el servicio "
                "y la profesional."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context={
                key: value
                for key, value in context.items()
                if key not in {"cart_payload", "availability_status"}
            },
            quick_replies=[build_missing_handoff_quick_reply(context)],
        )

    return build_guidance_response(
        message=(
            f"Perfecto. Dejé seleccionado {selected_service} con "
            f"{selected_professional}. Puedes abonar el 20% del servicio "
            "para avanzar con la reserva."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=deposit_context,
        next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
        cart_payload=cart_payload,
        quick_replies=[
            build_abono_quick_reply(deposit_context),
            build_other_services_quick_reply(selected_professional, deposit_context),
            build_restart_quick_reply(),
        ],
    )


def build_multi_service_selection_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    primary_service = read_primary_service_label(context)
    additional_service = read_context_string(
        context,
        "additional_service_candidate",
    )
    multi_context = {
        **context,
        "selected_service": primary_service,
        "primary_service": primary_service,
        "additional_service_candidate": additional_service,
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "service_selection_mode": "selecting_additional_service",
        "multi_service_decision_mode": True,
    }

    return build_guidance_response(
        message=(
            f"Ya tenías seleccionado {primary_service}. Ahora elegiste "
            f"{additional_service} como servicio adicional. ¿Quieres "
            f"preparar su abono o continuar solo con {primary_service}?"
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=multi_context,
        quick_replies=[
            build_primary_service_abono_quick_reply(
                primary_service,
                multi_context,
                action_type="reply",
                target=None,
            ),
            build_add_additional_service_to_cart_quick_reply(
                additional_service,
                multi_context,
            ),
            build_discard_additional_service_quick_reply(
                additional_service,
                multi_context,
            ),
            build_restart_quick_reply(),
        ],
    )


def build_add_additional_service_to_cart_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    primary_service = read_primary_service_label(context)
    additional_service = read_context_string(
        context,
        "additional_service_candidate",
    )
    cart_items = read_cart_item_service_labels(context)

    if additional_service and additional_service not in cart_items:
        cart_items.append(additional_service)

    cart_payload = build_booking_deposit_multi_service_cart_payload(
        {
            **context,
            "selected_service": primary_service,
            "primary_service": primary_service,
        },
        cart_items,
    )
    add_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "additional_service_candidate",
                "multi_service_decision_mode",
                "cart_payload",
                "availability_status",
            }
        },
        "selected_service": primary_service,
        "primary_service": primary_service,
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "service_selection_mode": True,
        "cart_items": cart_items,
        "cart_count": len(cart_items),
        "cart_payload": cart_payload,
    }

    if not primary_service or not additional_service:
        return build_guidance_response(
            message=(
                "Para agregar el servicio adicional necesito definir primero "
                "el servicio principal y el servicio adicional."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context=add_context,
            quick_replies=[build_missing_handoff_quick_reply(add_context)],
        )

    return build_guidance_response(
        message=(
            f"Preparé el abono del 20% de {additional_service}. Puedes "
            "revisar tu selección en el carrito, agregar más servicios o "
            "volver a iniciar."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=add_context,
        next_actions=[],
        cart_payload=cart_payload,
        quick_replies=[
            build_cart_navigation_quick_reply(add_context),
            build_add_more_services_quick_reply(add_context),
            build_restart_quick_reply(),
        ],
    )


def build_discard_additional_service_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    primary_service = read_primary_service_label(context)
    additional_service = read_context_string(
        context,
        "additional_service_candidate",
    )
    discard_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "additional_service_candidate",
                "multi_service_decision_mode",
                "cart_payload",
                "availability_status",
            }
        },
        "selected_service": primary_service,
        "primary_service": primary_service,
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "service_selection_mode": True,
    }

    if not primary_service or not additional_service:
        return build_guidance_response(
            message=(
                "Para descartar el servicio adicional necesito definir primero "
                "el servicio principal y el servicio adicional."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context=discard_context,
            quick_replies=[build_missing_handoff_quick_reply(discard_context)],
        )

    return build_guidance_response(
        message=(
            f"Perfecto. Descarté {additional_service} y mantuve "
            f"{primary_service} como servicio principal."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=discard_context,
        next_actions=[],
        quick_replies=[
            build_add_more_services_quick_reply(discard_context),
            build_restart_quick_reply(),
        ],
    )


def build_add_previous_service_to_cart_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    selected_service = read_context_string(context, "selected_service")
    previous_service = read_context_string(context, "previous_service")
    cart_items = read_cart_item_service_labels(context)

    if previous_service and previous_service not in cart_items:
        cart_items.append(previous_service)

    multi_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "previous_service",
                "multi_service_decision_mode",
                "cart_payload",
                "availability_status",
            }
        },
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "service_selection_mode": True,
        "cart_items": cart_items,
        "cart_count": len(cart_items),
    }

    if not previous_service or not selected_service:
        return build_guidance_response(
            message=(
                "Para agregar el servicio anterior necesito definir primero "
                "los servicios seleccionados."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context={
                key: value
                for key, value in context.items()
                if key
                not in {
                    "cart_payload",
                    "availability_status",
                    "multi_service_decision_mode",
                }
            },
            quick_replies=[build_missing_handoff_quick_reply(context)],
        )

    return build_guidance_response(
        message=(
            f"{previous_service} fue agregado al carrito. Ahora puedes "
            f"continuar con {selected_service}."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=multi_context,
        next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
        quick_replies=[
            build_selected_service_abono_quick_reply(
                selected_service,
                multi_context,
            ),
            build_restart_quick_reply(),
        ],
    )


def build_discard_previous_service_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    selected_professional = read_context_string(context, "selected_professional")
    selected_service = read_context_string(context, "selected_service")
    previous_service = read_context_string(context, "previous_service")
    discard_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "previous_service",
                "multi_service_decision_mode",
                "cart_payload",
                "cart_items",
                "cart_count",
                "availability_status",
            }
        },
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "service_selection_mode": True,
    }

    if not previous_service or not selected_service:
        return build_guidance_response(
            message=(
                "Para descartar el servicio anterior necesito definir primero "
                "los servicios seleccionados."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context=discard_context,
            quick_replies=[build_missing_handoff_quick_reply(discard_context)],
        )

    return build_guidance_response(
        message=(
            f"Perfecto. Descarté {previous_service} y dejé seleccionado "
            f"{selected_service} con {selected_professional}."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=discard_context,
        next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
        quick_replies=[
            build_selected_service_abono_quick_reply(
                selected_service,
                discard_context,
            ),
            build_restart_quick_reply(),
        ],
    )


def build_new_service_payment_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    selected_service = read_context_string(context, "selected_service")
    service_labels = build_selected_service_payment_labels(context, selected_service)
    cart_payload = build_booking_deposit_multi_service_cart_payload(
        context,
        service_labels,
    )
    payment_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "previous_service",
                "multi_service_decision_mode",
            }
        },
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "availability_status": "pending_schedule_selection",
        "cart_payload": cart_payload,
        "cart_items": service_labels,
        "cart_count": len(service_labels),
    }

    if cart_payload is None:
        return build_guidance_response(
            message=(
                "Para preparar el abono necesito definir primero el servicio "
                "y la profesional."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context={
                key: value
                for key, value in context.items()
                if key not in {"cart_payload", "availability_status"}
            },
            quick_replies=[build_missing_handoff_quick_reply(context)],
        )

    return build_guidance_response(
        message=(
            f"Preparé el abono del 20% de {selected_service}. Puedes "
            "revisarlo en el carrito."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=payment_context,
        next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
        redirect_target=BOOKING_DEPOSIT_REDIRECT_TARGET,
        cart_payload=cart_payload,
        quick_replies=[build_cart_handoff_quick_reply(payment_context)],
    )


def build_primary_service_payment_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    primary_service = read_primary_service_label(context)
    service_labels = build_primary_service_payment_labels(context, primary_service)
    cart_payload = build_booking_deposit_multi_service_cart_payload(
        {
            **context,
            "selected_service": primary_service,
            "primary_service": primary_service,
            "checkout_ready": True,
            "conversation_locked": True,
        },
        service_labels,
    )
    payment_context = {
        **{
            key: value
            for key, value in context.items()
            if key
            not in {
                "additional_service_candidate",
                "previous_service",
                "multi_service_decision_mode",
            }
        },
        "selected_service": primary_service,
        "primary_service": primary_service,
        "flow_step": AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        "availability_status": "pending_schedule_selection",
        "cart_payload": cart_payload,
        "cart_items": service_labels,
        "cart_count": len(service_labels),
    }

    if cart_payload is None:
        return build_guidance_response(
            message=(
                "Para preparar el abono necesito definir primero el servicio "
                "principal y la profesional."
            ),
            flow_step=AssistantFlowStep.SERVICE_SELECTION.value,
            context={
                key: value
                for key, value in context.items()
                if key not in {"cart_payload", "availability_status"}
            },
            quick_replies=[build_missing_handoff_quick_reply(context)],
        )

    is_multi_service_flow = bool(
        read_cart_item_service_labels(context)
        or read_context_bool(context, "service_selection_mode")
        or read_context_bool(context, "multi_service_decision_mode")
    )

    if is_multi_service_flow:
        return build_multi_service_checkout_ready_guidance(payment_context)

    return build_guidance_response(
        message=(
            f"Preparé el abono del 20% de {primary_service}. Puedes "
            "revisarlo en el carrito."
        ),
        flow_step=AssistantFlowStep.DEPOSIT_CONFIRMATION.value,
        context=payment_context,
        next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
        redirect_target=BOOKING_DEPOSIT_REDIRECT_TARGET,
        cart_payload=cart_payload,
        quick_replies=[build_cart_handoff_quick_reply(payment_context)],
    )


def build_service_change_abono_guidance(
    context: dict[str, object],
) -> dict[str, object]:
    selected_professional = read_context_string(context, "selected_professional")
    selected_service = read_context_string(context, "selected_service")
    requested_day = read_context_string(context, "requested_day")
    requested_time = read_context_string(context, "requested_time")
    cart_payload = build_booking_deposit_cart_payload("pagar abono", context)
    abono_context = {
        **context,
        "flow_step": AssistantFlowStep.AVAILABILITY_CHECK.value,
        "availability_status": "available",
        "cart_payload": cart_payload,
    }

    if cart_payload is None:
        return build_guidance_response(
            message=build_time_selection_message(
                selected_professional,
                selected_service,
            ),
            flow_step=AssistantFlowStep.TIME_SELECTION.value,
            context={
                key: value
                for key, value in context.items()
                if key not in {"cart_payload", "availability_status"}
            },
            quick_replies=build_time_selection_quick_replies(context),
        )

    return build_guidance_response(
        message=(
            f"Perfecto. Cambié el servicio a {selected_service} con "
            f"{selected_professional} para el {requested_day} a las "
            f"{requested_time}. ¿Quieres avanzar con el abono del 20%?"
        ),
        flow_step=AssistantFlowStep.AVAILABILITY_CHECK.value,
        context=abono_context,
        next_actions=[BOOKING_DEPOSIT_TERMS_NOTICE],
        cart_payload=cart_payload,
        quick_replies=[
            build_abono_quick_reply(abono_context),
            build_other_services_quick_reply(selected_professional, abono_context),
            (
                build_restart_quick_reply()
                if selected_professional == PROFESSIONAL_MARIA_IGNACIA
                else build_nadia_agenda_quick_reply(abono_context, include_service=True)
            ),
        ],
    )


def build_missing_handoff_quick_reply(context: dict[str, object]) -> dict[str, object]:
    return build_quick_reply(
        label="Ir a reservar",
        message="Quiero ir a reservas para elegir servicio y profesional",
        action_type="navigate",
        target="/booking",
        payload={"reason": "missing_booking_deposit_data"},
        context=context,
    )


def build_restart_quick_reply() -> dict[str, object]:
    return build_quick_reply(
        label="Volver a iniciar",
        message="Volver a iniciar",
        action_type="reply",
        payload={"reason": "assistant_restart"},
        context=build_reset_context(),
    )


def build_reset_context() -> dict[str, object]:
    return {
        "intent": "general",
        "flow_step": AssistantFlowStep.COMPLETED.value,
    }


def build_initial_conversation_quick_replies() -> list[dict[str, object]]:
    reset_context = build_reset_context()

    return [
        build_quick_reply(
            label="Reservar hora",
            message="Quiero reservar una hora",
            action_type="reply",
            payload={"reason": "booking_start"},
            context=reset_context,
        ),
        build_quick_reply(
            label="Ver servicios",
            message="Quiero ver todos los servicios disponibles",
            action_type="navigate",
            target="/services",
            payload={"reason": "full_services_catalog"},
            context=reset_context,
        ),
        build_quick_reply(
            label="Ver productos",
            message="Quiero comprar productos",
            action_type="navigate",
            target="/products",
            payload={"reason": "product_start"},
            context=reset_context,
        ),
    ]


def build_assistant_restart_guidance() -> dict[str, object]:
    reset_context = build_reset_context()

    return {
        "message": (
            "Hola, soy la asistente virtual de Always Beautiful. Puedo "
            "ayudarte a reservar una hora, revisar servicios o ver productos. "
            "¿Qué quieres hacer?"
        ),
        "professionals": [],
        "next_actions": [
            "Puedes iniciar una reserva guiada desde el chat.",
            "También puedes pedir orientación de productos.",
        ],
        "quick_replies": build_initial_conversation_quick_replies(),
        "redirect_target": None,
        "cart_payload": None,
        "context": reset_context,
        "flow_step": AssistantFlowStep.COMPLETED.value,
    }


def is_complete_booking_deposit_cart_payload(value: object) -> bool:
    if not isinstance(value, dict):
        return False

    schedule_status = value.get("schedule_status")
    has_valid_schedule_status = schedule_status in {
        "pending_selection",
        "pending_confirmation",
    }
    has_valid_schedule_detail = (
        bool(value.get("requested_day") and value.get("requested_time"))
        if schedule_status == "pending_confirmation"
        else True
    )

    return bool(
        value.get("type") == "booking_deposit"
        and value.get("status") == "pending_deposit"
        and value.get("deposit_percentage") == BOOKING_DEPOSIT_PERCENTAGE
        and value.get("remaining_percentage") == 100 - BOOKING_DEPOSIT_PERCENTAGE
        and value.get("service_label")
        and value.get("professional_label")
        and value.get("selected_service")
        and value.get("selected_professional")
        and value.get("professional_id")
        and value.get("professional_role")
        and has_valid_schedule_status
        and has_valid_schedule_detail
        and value.get("confirmation_status") == "not_confirmed"
        and value.get("payment_status") == "deposit_pending"
    )


def get_contextual_incompatibility(
    context: dict[str, object],
) -> dict[str, object] | None:
    selected_professional = read_context_string(context, "selected_professional")
    selected_service = read_context_string(context, "selected_service")

    if not selected_professional or not selected_service:
        return None

    if (
        selected_professional == PROFESSIONAL_NADIA_LUISA
        and detect_service_category(selected_service) == SERVICE_CATEGORY_COSMETOLOGY
    ):
        return {
            "professional": PROFESSIONAL_NADIA_LUISA,
            "alternative_professional": PROFESSIONAL_MARIA_IGNACIA,
            "message": (
                "Nadia Luisa no realiza servicios de cosmetología. Para ese "
                "servicio puede atenderte María Ignacia."
            ),
        }

    return None


def wants_booking_start(message: str, context: dict[str, object]) -> bool:
    return (
        detects_booking_intent(message)
        and read_context_string(context, "selected_professional") is None
        and read_context_string(context, "selected_service") is None
        and read_context_string(context, "requested_day") is None
        and read_context_string(context, "requested_time") is None
    )


def detects_maria_more_services_intent(message: str) -> bool:
    normalized_message = normalize_message_text(message)
    wants_more_services = (
        "ver mas servicios" in normalized_message
        or "ver todos los servicios" in normalized_message
        or "todos los servicios" in normalized_message
        or "mas servicios" in normalized_message
        or "otros servicios" in normalized_message
    )
    references_maria = (
        "maria" in normalized_message
        or "ignacia" in normalized_message
    )

    return wants_more_services and references_maria


def detects_change_service_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)

    if "cambiar servicio" in normalized_message:
        return True

    if isinstance(context, dict):
        has_selected_service = read_previous_service_label(context) is not None
        wants_professional_services = (
            "ver todos los servicios" in normalized_message
            or "todos los servicios" in normalized_message
            or "ver mas servicios" in normalized_message
            or "mas servicios" in normalized_message
            or "otros servicios" in normalized_message
        )

        if has_selected_service and wants_professional_services:
            return True

        return read_context_string(context, "reason") == "change_service"

    return False


def detects_add_previous_service_to_cart_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)
    previous_service = read_context_string(context or {}, "previous_service")
    selected_professional = read_context_string(
        context or {},
        "selected_professional",
    )

    if selected_professional and selected_professional != PROFESSIONAL_MARIA_IGNACIA:
        return False

    if (
        previous_service
        and "agregar" in normalized_message
        and "carrito" in normalized_message
        and normalize_message_text(previous_service) in normalized_message
    ):
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == (
            "add_previous_service_to_cart"
        )

    return False


def detects_add_additional_service_to_cart_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)
    additional_service = read_context_string(
        context or {},
        "additional_service_candidate",
    )
    selected_professional = read_context_string(
        context or {},
        "selected_professional",
    )

    if selected_professional and selected_professional != PROFESSIONAL_MARIA_IGNACIA:
        return False

    has_additional_service_payment_intent = (
        "abonar 20% de" in normalized_message
        or "ir a pagar 20% de" in normalized_message
        or "pagar 20% de" in normalized_message
    )

    if (
        additional_service
        and has_additional_service_payment_intent
        and normalize_message_text(additional_service) in normalized_message
    ):
        return True

    if (
        additional_service
        and "agregar" in normalized_message
        and normalize_message_text(additional_service) in normalized_message
    ):
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == (
            "add_additional_service_to_cart"
        )

    return False


def detects_discard_previous_service_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)
    previous_service = read_context_string(context or {}, "previous_service")
    selected_professional = read_context_string(
        context or {},
        "selected_professional",
    )

    if selected_professional and selected_professional != PROFESSIONAL_MARIA_IGNACIA:
        return False

    if (
        previous_service
        and "descartar" in normalized_message
        and normalize_message_text(previous_service) in normalized_message
    ):
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == "discard_previous_service"

    return False


def detects_discard_additional_service_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)
    additional_service = read_context_string(
        context or {},
        "additional_service_candidate",
    )
    selected_professional = read_context_string(
        context or {},
        "selected_professional",
    )

    if selected_professional and selected_professional != PROFESSIONAL_MARIA_IGNACIA:
        return False

    if (
        additional_service
        and "descartar" in normalized_message
        and normalize_message_text(additional_service) in normalized_message
    ):
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == "discard_additional_service"

    return False


def detects_new_service_payment_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)
    has_selected_service_payment_intent = (
        "abonar 20% de" in normalized_message
        or "ir a pagar 20% de" in normalized_message
        or "pagar 20% de" in normalized_message
    )

    if has_selected_service_payment_intent and read_previous_service_label(context):
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == "pay_selected_service"

    return False


def detects_primary_service_payment_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)
    primary_service = read_primary_service_label(context)

    if not primary_service:
        return False

    has_primary_service_payment_intent = (
        "abonar 20% de" in normalized_message
        or "ir a pagar 20% de" in normalized_message
        or "pagar 20% de" in normalized_message
    )

    if (
        has_primary_service_payment_intent
        and normalize_message_text(primary_service) in normalized_message
    ):
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == "pay_primary_service"

    return False


def has_multi_service_selection(context: dict[str, object]) -> bool:
    primary_service = read_primary_service_label(context)
    additional_service = read_context_string(
        context,
        "additional_service_candidate",
    )
    selected_professional = read_context_string(context, "selected_professional")

    return bool(
        selected_professional == PROFESSIONAL_MARIA_IGNACIA
        and primary_service
        and additional_service
        and primary_service != additional_service
        and (
            read_context_bool(context, "service_change_mode")
            or read_context_bool(context, "service_selection_mode")
        )
    )


def detects_assistant_restart_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)

    if normalized_message in {
        "volver a iniciar",
        "reiniciar",
        "reiniciar asistente",
        "empezar de nuevo",
        "comenzar de nuevo",
    }:
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == "assistant_restart"

    return False


def detects_cart_redirect_intent(
    message: str,
    context: dict[str, object] | None,
) -> bool:
    normalized_message = normalize_message_text(message)

    if normalized_message == "ir a carrito de compras":
        return True

    if isinstance(context, dict):
        return read_context_string(context, "reason") == "open_cart"

    return False


def detects_professional_services_navigation(
    message: str,
    context: dict[str, object] | None,
    booking_context: dict[str, object],
) -> bool:
    normalized_message = normalize_message_text(message)
    selected_professional = read_context_string(
        booking_context,
        "selected_professional",
    )

    if not selected_professional:
        return False

    if isinstance(context, dict) and read_context_string(
        context,
        "reason",
    ) == "professional_services_catalog":
        return True

    return "servicios" in normalized_message and (
        "nadia" in normalized_message
        or "maria" in normalized_message
        or "ignacia" in normalized_message
    )


def build_service_change_context(
    context: dict[str, object],
) -> dict[str, object]:
    previous_service = read_previous_service_label(context)
    selected_professional = read_context_string(context, "selected_professional")
    service_change_context = {
        key: value
        for key, value in context.items()
        if key
        not in {
            "availability_status",
            "cart_payload",
            "reason",
        }
    }

    if previous_service:
        service_change_context["previous_service"] = previous_service

        if selected_professional == PROFESSIONAL_MARIA_IGNACIA:
            primary_service = read_primary_service_label(service_change_context)
            service_change_context["primary_service"] = previous_service
            service_change_context["selected_service"] = (
                read_context_string(context, "selected_service") or previous_service
            )
            service_change_context["service_selection_mode"] = (
                "selecting_additional_service"
                if primary_service
                else True
            )
        else:
            service_change_context.pop("selected_service", None)

    return service_change_context | {
        "flow_step": AssistantFlowStep.SERVICE_SELECTION.value,
        "service_change_mode": True,
        "service_selection_mode": (
            "selecting_additional_service"
            if selected_professional == PROFESSIONAL_MARIA_IGNACIA
            and read_primary_service_label(service_change_context)
            else True
        ),
        "deposit_required": True,
        "deposit_percentage": BOOKING_DEPOSIT_PERCENTAGE,
    }


def read_previous_service_label(context: dict[str, object] | None) -> str | None:
    if not isinstance(context, dict):
        return None

    previous_service = read_context_string(context, "previous_service")

    if previous_service:
        return previous_service

    selected_service = read_context_string(context, "selected_service")

    if selected_service:
        return selected_service

    cart_payload = context.get("cart_payload")

    if isinstance(cart_payload, dict):
        value = cart_payload.get("service_label")

        if isinstance(value, str) and value.strip():
            return value.strip()

    nested_context = context.get("context")

    if isinstance(nested_context, dict):
        return read_previous_service_label(nested_context)

    return None


def read_primary_service_label(context: dict[str, object] | None) -> str | None:
    if not isinstance(context, dict):
        return None

    primary_service = read_context_string(context, "primary_service")

    if primary_service:
        return primary_service

    selected_service = read_context_string(context, "selected_service")

    if selected_service:
        return selected_service

    previous_service = read_context_string(context, "previous_service")

    if previous_service:
        return previous_service

    nested_context = context.get("context")

    if isinstance(nested_context, dict):
        return read_primary_service_label(nested_context)

    return None


def read_cart_item_service_labels(context: dict[str, object] | None) -> list[str]:
    if not isinstance(context, dict):
        return []

    raw_cart_items = context.get("cart_items")

    if not isinstance(raw_cart_items, list):
        return []

    service_labels: list[str] = []

    for item in raw_cart_items:
        service_label = None

        if isinstance(item, str):
            service_label = item.strip()
        elif isinstance(item, dict):
            service_label = read_context_string(item, "service_label")

        if service_label and service_label not in service_labels:
            service_labels.append(service_label)

    return service_labels


def build_selected_service_payment_labels(
    context: dict[str, object],
    selected_service: str | None,
) -> list[str]:
    service_labels = read_cart_item_service_labels(context)

    if selected_service and selected_service not in service_labels:
        service_labels.append(selected_service)

    return service_labels


def build_primary_service_payment_labels(
    context: dict[str, object],
    primary_service: str | None,
) -> list[str]:
    service_labels = read_cart_item_service_labels(context)

    if primary_service and primary_service not in service_labels:
        service_labels.append(primary_service)

    return service_labels


def build_change_service_message(
    professional_label: str,
    previous_service: str | None,
) -> str:
    service_fragment = (
        f"{previous_service} estaba seleccionado. "
        if previous_service
        else ""
    )

    return (
        f"{service_fragment}Puedes elegir otro servicio de {professional_label} "
        "o revisar todos sus servicios."
    )


def build_professional_services_navigation_message(professional_label: str) -> str:
    return (
        f"Te llevé a la sección de Servicios con los servicios de "
        f"{professional_label}. También puedes elegir un servicio rápido o "
        "revisar su agenda."
    )


def is_nadia_quick_schedule(context: dict[str, object]) -> bool:
    selected_professional = read_context_string(context, "selected_professional")
    requested_day = read_context_string(context, "requested_day")
    requested_time = read_context_string(context, "requested_time")

    return (
        selected_professional == PROFESSIONAL_NADIA_LUISA
        and any(
            requested_day == quick_day and requested_time == quick_time
            for _, quick_day, quick_time in NADIA_QUICK_SCHEDULES
        )
    )


def is_selecting_additional_service_mode(
    context: dict[str, object] | None,
) -> bool:
    if not isinstance(context, dict):
        return False

    service_selection_mode = context.get("service_selection_mode")

    if isinstance(service_selection_mode, str):
        return service_selection_mode == "selecting_additional_service"

    return bool(service_selection_mode) and bool(
        read_context_string(context, "primary_service")
        and read_context_string(context, "additional_service_candidate")
    )


def read_context_bool(
    context: dict[str, object],
    key: str,
) -> bool:
    return bool(context.get(key) is True)


def is_professional_selection_only(
    message: str,
    context: dict[str, object],
) -> bool:
    selected_professional = read_context_string(context, "selected_professional")

    if selected_professional is None:
        return False

    return (
        read_context_string(context, "selected_service") is None
        and read_context_string(context, "requested_day") is None
        and read_context_string(context, "requested_time") is None
        and not detects_booking_intent(message)
    )


def build_professional_services_message(professional_label: str | None) -> str:
    if professional_label == PROFESSIONAL_NADIA_LUISA:
        return (
            "Nadia Luisa atiende servicios de estilismo profesional. Puedes "
            "elegir un servicio rápido o revisar toda su agenda."
        )

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return (
            "María Ignacia atiende cosmetología, maquillaje y estilismo. "
            "Estos son algunos servicios destacados."
        )

    return "Estos son algunos servicios destacados."


def build_time_selection_message(
    professional_label: str | None,
    service_label: str | None,
) -> str:
    if professional_label == PROFESSIONAL_NADIA_LUISA and service_label:
        return (
            f"Perfecto. Nadia Luisa puede atenderte para {service_label}. "
            "Elige un horario rápido o revisa toda su agenda."
        )

    if professional_label == PROFESSIONAL_MARIA_IGNACIA and service_label:
        return (
            f"Perfecto. María Ignacia puede atenderte para {service_label}. "
            "Estos horarios son simulados de solo lectura y quedan sujetos "
            "a confirmación operativa del salón."
        )

    return (
        "Perfecto. Ya tengo profesional y servicio. Puedes elegir un horario "
        "rápido o revisar la agenda completa."
    )


def build_context_message(context: dict[str, object]) -> str:
    parts = [
        "Quiero reservar",
        read_context_string(context, "selected_service") or "",
        (
            f"con {read_context_string(context, 'selected_professional')}"
            if read_context_string(context, "selected_professional")
            else ""
        ),
        (
            f"el {read_context_string(context, 'requested_day')}"
            if read_context_string(context, "requested_day")
            else ""
        ),
        (
            f"a las {read_context_string(context, 'requested_time')}"
            if read_context_string(context, "requested_time")
            else ""
        ),
    ]

    return " ".join(part for part in parts if part)


def normalize_professional_id(value: str | None) -> str | None:
    if value is None:
        return None

    normalized_value = normalize_message_text(value)

    if normalized_value in {
        "nadia",
        "nadia luisa",
        "nadia_luisa",
        "nadia-luisa",
    }:
        return PROFESSIONAL_NADIA_LUISA

    if normalized_value in {
        "maria",
        "maria ignacia",
        "maria_ignacia",
        "maria-ignacia",
        "ignacia",
    }:
        return PROFESSIONAL_MARIA_IGNACIA

    if value in {PROFESSIONAL_NADIA_LUISA, PROFESSIONAL_MARIA_IGNACIA}:
        return value

    return None


def professional_to_payload_id(professional_label: str) -> str:
    if professional_label == PROFESSIONAL_NADIA_LUISA:
        return "nadia_luisa"

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return "maria_ignacia"

    return "unknown"


def professional_role_for_label(professional_label: str) -> str | None:
    if professional_label == PROFESSIONAL_NADIA_LUISA:
        return PROFESSIONAL_STYLIST

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return PROFESSIONAL_COSMETOLOGIST

    return None


def professional_short_name(professional_label: str) -> str:
    if professional_label == PROFESSIONAL_NADIA_LUISA:
        return "Nadia"

    if professional_label == PROFESSIONAL_MARIA_IGNACIA:
        return "María"

    return professional_label


def read_context_string(
    context: dict[str, object],
    key: str,
) -> str | None:
    value = context.get(key)

    if isinstance(value, str) and value.strip():
        return value.strip()

    return None
