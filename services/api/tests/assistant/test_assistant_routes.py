from pathlib import Path

from fastapi.testclient import TestClient

from app.assistant.policies import BOOKING_DEPOSIT_PERCENTAGE
from app.assistant.state import AssistantFlowStep, AssistantIntent
from app.main import app


client = TestClient(app)
REPO_ROOT = Path(__file__).resolve().parents[4]

FORBIDDEN_REAL_COMMITMENT_COPY = (
    "reserva confirmada",
    "hora confirmada",
    "cita agendada",
    "pago confirmado",
    "pago realizado",
)

VALID_QUICK_REPLY_ACTION_TYPES = {"reply", "navigate", "cart_handoff"}
PENDING_NOTICE = "La hora queda pendiente hasta confirmación del salón y abono web."
DEPOSIT_TERMS_NOTICE = (
    "Al continuar, aceptas los términos y condiciones, la política de "
    "privacidad y las condiciones de reserva de Always Beautiful. El abono "
    "corresponde al 20% y la hora queda pendiente hasta confirmación "
    "operativa. El saldo restante del 80% deberá pagarse según las "
    "condiciones informadas por el salón. El comprobante y las instrucciones "
    "de pago del saldo restante serán enviados al correo registrado."
)


def stringify_payload(value):
    if isinstance(value, dict):
        return " ".join(stringify_payload(item) for item in value.values())

    if isinstance(value, list):
        return " ".join(stringify_payload(item) for item in value)

    return str(value)


def assert_no_real_commitment_copy(body):
    combined_text = (
        f"{body.get('message', '')} "
        f"{' '.join(body.get('next_actions', []))} "
        f"{stringify_payload(body.get('quick_replies', []))} "
        f"{stringify_payload(body.get('cart_payload') or {})}"
    ).lower()

    for forbidden_copy in FORBIDDEN_REAL_COMMITMENT_COPY:
        assert forbidden_copy not in combined_text


def assert_pending_notice_not_duplicated(body):
    visual_text = (
        f"{body.get('message', '')} "
        f"{' '.join(body.get('next_actions', []))}"
    )

    assert visual_text.count(PENDING_NOTICE) <= 1


def assert_deposit_terms_notice_not_duplicated(body):
    visual_text = (
        f"{body.get('message', '')} "
        f"{' '.join(body.get('next_actions', []))}"
    )

    assert visual_text.count(DEPOSIT_TERMS_NOTICE) <= 1


def post_assistant(
    message: str,
    session_id: str = "assistant-test",
    context: dict | None = None,
):
    payload = {
        "session_id": session_id,
        "message": message,
        "channel": "web",
    }

    if context is not None:
        payload["context"] = context

    return client.post("/assistant/chat", json=payload)


def quick_labels(body):
    return [quick_reply["label"] for quick_reply in body["quick_replies"]]


def find_quick_reply(body, label):
    return next(
        quick_reply
        for quick_reply in body["quick_replies"]
        if quick_reply["label"] == label
    )


def assert_service_selection_deposit_response(
    body,
    service_label,
    professional_label,
    professional_id,
    professional_role,
):
    labels = quick_labels(body)
    cart_payload = body["cart_payload"]
    abono_reply = find_quick_reply(body, "Abonar 20% del servicio")
    other_services_label = (
        "Ver todos los servicios de María Ignacia"
        if professional_label == "María Ignacia"
        else f"Ver todos los servicios de {professional_label.split()[0]}"
    )

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["flow_step"] == AssistantFlowStep.DEPOSIT_CONFIRMATION.value
    assert body["message"] == (
        f"Perfecto. Dejé seleccionado {service_label} con "
        f"{professional_label}. Puedes abonar el 20% del servicio para "
        "avanzar con la reserva."
    )
    assert labels == [
        "Abonar 20% del servicio",
        other_services_label,
        "Volver a iniciar",
    ]
    assert service_label not in labels
    assert "Ver otros servicios de María" not in labels
    assert "Ver otros servicios de Nadia" not in labels
    assert "Ver más servicios de María" not in labels
    assert "Agendar ahora" not in labels
    assert cart_payload["type"] == "booking_deposit"
    assert cart_payload["status"] == "pending_deposit"
    assert cart_payload["deposit_percentage"] == 20
    assert cart_payload["remaining_percentage"] == 80
    assert cart_payload["amount_status"] == "pending_final_price"
    assert cart_payload["service_label"] == service_label
    assert cart_payload["professional_label"] == professional_label
    assert cart_payload["selected_service"] == service_label
    assert cart_payload["selected_professional"] == professional_label
    assert cart_payload["professional_id"] == professional_id
    assert cart_payload["professional_role"] == professional_role
    assert cart_payload["requested_day"] is None
    assert cart_payload["requested_time"] is None
    assert cart_payload["schedule_status"] in {
        "pending_selection",
        "pending_confirmation",
    }
    assert cart_payload["confirmation_status"] == "not_confirmed"
    assert cart_payload["payment_status"] == "deposit_pending"
    assert len(cart_payload["items"]) == 1
    assert cart_payload["total_items"] == 1
    assert cart_payload["cart_count"] == 1
    assert cart_payload["items"][0]["professional"] == professional_label
    assert cart_payload["items"][0]["professional_id"] == professional_id
    assert cart_payload["items"][0]["professional_role"] == professional_role
    assert cart_payload["items"][0]["service_label"] == service_label
    assert cart_payload["items"][0]["deposit_percentage"] == 20
    assert cart_payload["items"][0]["remaining_percentage"] == 80
    assert cart_payload["items"][0]["amount_status"] == "pending_final_price"
    assert "deposit_amount" not in cart_payload["items"][0]
    assert "remaining_amount" not in cart_payload["items"][0]
    assert abono_reply["target"] == "/cart"
    assert abono_reply["payload"]["cart_payload"]["schedule_status"] in {
        "pending_selection",
        "pending_confirmation",
    }
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def assert_quick_replies_contract(body):
    quick_replies = body["quick_replies"]

    assert isinstance(quick_replies, list)
    assert quick_replies

    for quick_reply in quick_replies:
        assert isinstance(quick_reply["label"], str)
        assert 1 <= len(quick_reply["label"]) <= 32
        assert isinstance(quick_reply["message"], str)
        assert quick_reply["message"].strip()
        assert quick_reply["action_type"] in VALID_QUICK_REPLY_ACTION_TYPES
        assert quick_reply["target"] is None or isinstance(
            quick_reply["target"],
            str,
        )
        assert quick_reply["payload"] is None or isinstance(
            quick_reply["payload"],
            dict,
        )


def test_assistant_health():
    response = client.get("/assistant/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "module": "assistant"}


def test_assistant_prepares_booking_conversion_intent_without_activating_it():
    assert AssistantIntent.BOOKING_CONVERSION.value == "booking_conversion"


def test_assistant_chat_returns_structured_quick_replies():
    response = post_assistant("Hola", "general-session")

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.GENERAL.value
    assert body["message"] == (
        "Hola, soy la asistente virtual de Always Beautiful. Puedo ayudarte a "
        "reservar una hora, revisar servicios o ver productos. ¿Qué "
        "quieres hacer?"
    )
    assert quick_labels(body) == ["Reservar hora", "Ver servicios", "Ver productos"]
    assert find_quick_reply(body, "Ver servicios")["target"] == "/services"
    assert find_quick_reply(body, "Ver productos")["target"] == "/products"
    assert_quick_replies_contract(body)
    assert_no_real_commitment_copy(body)


def test_services_navigation_returns_commercial_options_without_loop():
    response = post_assistant(
        "Ver servicios",
        "services-navigation-session",
        context={"reason": "full_services_catalog"},
    )

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == (
        "De las dos profesionales que atienden en el salón de belleza, "
        "¿qué servicios deseas revisar?"
    )
    assert quick_labels(body) == [
        "Nadia Luisa",
        "Maria Ignacia",
        "Volver a iniciar",
    ]
    assert find_quick_reply(body, "Nadia Luisa")["target"] == (
        "/services?professional=nadia_luisa"
    )
    assert find_quick_reply(body, "Maria Ignacia")["target"] == (
        "/services?professional=maria_ignacia"
    )
    assert find_quick_reply(body, "Volver a iniciar")["payload"]["reason"] == (
        "assistant_restart"
    )
    assert "Ver todos los servicios" not in quick_labels(body)
    assert "Servicios de Nadia" not in quick_labels(body)
    assert "Servicios de Maria" not in quick_labels(body)
    assert "Reservar hora" not in quick_labels(body)
    assert "Ver productos" not in quick_labels(body)
    assert_no_real_commitment_copy(body)


def test_services_navigation_keeps_legacy_aliases_for_existing_sessions():
    nadia_response = post_assistant(
        "Servicios de Nadia",
        "legacy-services-nadia-session",
    )
    maria_response = post_assistant(
        "Servicios de Maria",
        "legacy-services-maria-session",
    )

    assert nadia_response.status_code == 200
    nadia_body = nadia_response.json()
    assert nadia_body["context"]["selected_professional"] == "Nadia Luisa"
    assert quick_labels(nadia_body) == [
        "Corte profesional",
        "Brushing profesional",
        "Peinado social",
        "Tratamiento capilar",
        "Coloración / raíz",
        "Ver toda la agenda de Nadia",
    ]
    assert "Servicios de Nadia" not in quick_labels(nadia_body)
    assert_no_real_commitment_copy(nadia_body)

    assert maria_response.status_code == 200
    maria_body = maria_response.json()
    assert maria_body["context"]["selected_professional"] == "María Ignacia"
    assert quick_labels(maria_body) == [
        "Limpieza facial",
        "Perfilado de cejas",
        "Laminado de cejas",
        "Hidratación facial",
        "Maquillaje",
        "Peinados femeninos",
        "Brushing",
        "Tratamiento capilar",
        "Ver todos los servicios de María Ignacia",
        "Volver a iniciar",
    ]
    assert "Servicios de Maria" not in quick_labels(maria_body)
    assert_no_real_commitment_copy(maria_body)


def test_next_actions_and_quick_replies_are_not_mixed():
    response = post_assistant("Quiero reservar", "booking-separation-session")

    assert response.status_code == 200
    body = response.json()
    labels = set(quick_labels(body))

    assert all(isinstance(action, str) for action in body["next_actions"])
    assert all(isinstance(reply, dict) for reply in body["quick_replies"])
    assert not any(action in labels for action in body["next_actions"])
    assert_quick_replies_contract(body)
    assert_no_real_commitment_copy(body)


def test_booking_intent_offers_professionals():
    response = post_assistant("Quiero reservar", "booking-start-session")

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert body["message"] == (
        "Perfecto. Te ayudo a avanzar con la reserva. Primero elige con qué "
        "profesional deseas atenderte."
    )
    assert quick_labels(body) == [
        "Nadia Luisa",
        "María Ignacia",
    ]
    assert "No estoy segura" not in quick_labels(body)
    assert_no_real_commitment_copy(body)


def test_nadia_featured_services_are_styling_only():
    response = post_assistant("Nadia Luisa", "nadia-featured-session")

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["message"] == (
        "Nadia Luisa atiende servicios de estilismo profesional. Puedes "
        "elegir un servicio rápido o revisar toda su agenda."
    )
    assert quick_labels(body) == [
        "Corte profesional",
        "Brushing profesional",
        "Peinado social",
        "Tratamiento capilar",
        "Coloración / raíz",
        "Ver toda la agenda de Nadia",
    ]
    forbidden_nadia_labels = {
        "Limpieza facial",
        "Hidratación facial",
        "Diagnóstico facial",
        "Perfilado de cejas",
        "Laminado de cejas",
    }

    assert forbidden_nadia_labels.isdisjoint(set(quick_labels(body)))
    assert find_quick_reply(body, "Ver toda la agenda de Nadia")["target"] == (
        "/booking?professional=nadia_luisa"
    )
    assert_no_real_commitment_copy(body)


def test_nadia_service_selection_moves_to_deposit_without_relisting_services():
    professional_response = post_assistant(
        "Nadia Luisa",
        "nadia-service-selection-session",
    )
    professional_body = professional_response.json()
    service_reply = find_quick_reply(professional_body, "Peinado social")

    response = post_assistant(
        service_reply["message"],
        "nadia-service-selection-session",
        context=service_reply["payload"],
    )

    assert response.status_code == 200
    body = response.json()

    assert body["context"]["selected_professional"] == "Nadia Luisa"
    assert body["context"]["professional_id"] == "nadia_luisa"
    assert body["context"]["professional_role"] == "Estilista profesional"
    assert body["context"]["selected_service"] == "Peinado social"
    assert {
        "Corte profesional",
        "Brushing profesional",
        "Peinado social",
        "Tratamiento capilar",
        "Coloración / raíz",
    }.isdisjoint(quick_labels(body))
    assert_service_selection_deposit_response(
        body,
        "Peinado social",
        "Nadia Luisa",
        "nadia_luisa",
        "Estilista profesional",
    )


def test_nadia_schedule_selection_allows_cart_handoff_with_complete_payload():
    response = post_assistant(
        "Quiero reservar Peinado social con Nadia Luisa el miércoles a las 10:00",
        "nadia-schedule-handoff-session",
    )

    assert response.status_code == 200
    body = response.json()
    quick_reply = find_quick_reply(body, "Abonar 20% del servicio")

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["flow_step"] == AssistantFlowStep.AVAILABILITY_CHECK.value
    assert body["cart_payload"]["type"] == "booking_deposit"
    assert body["cart_payload"]["professional_label"] == "Nadia Luisa"
    assert body["cart_payload"]["service_label"] == "Peinado social"
    assert body["cart_payload"]["requested_day"] == "miércoles"
    assert body["cart_payload"]["requested_time"] == "10:00"
    assert body["cart_payload"]["deposit_percentage"] == 20
    assert body["cart_payload"]["remaining_percentage"] == 80
    assert body["cart_payload"]["schedule_status"] == "pending_confirmation"
    assert body["cart_payload"]["payment_status"] == "deposit_pending"
    assert quick_reply["target"] == "/cart"
    assert quick_reply["payload"]["cart_payload"]["confirmation_status"] == (
        "not_confirmed"
    )
    assert find_quick_reply(body, "Ver toda la agenda de Nadia")["target"] == (
        "/booking?professional=nadia_luisa"
    )
    assert_no_real_commitment_copy(body)


def test_nadia_services_navigation_returns_quick_services_not_generic_loop():
    response = post_assistant(
        "Quiero ver todos los servicios de Nadia Luisa",
        "nadia-services-navigation-session",
        context={
            "reason": "professional_services_catalog",
            "selected_professional": "Nadia Luisa",
            "professional_id": "nadia_luisa",
            "professional_role": "Estilista profesional",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == (
        "Te llevé a la sección de Servicios con los servicios de Nadia Luisa. "
        "También puedes elegir un servicio rápido o revisar su agenda."
    )
    assert body["context"]["selected_professional"] == "Nadia Luisa"
    assert quick_labels(body) == [
        "Corte profesional",
        "Brushing profesional",
        "Peinado social",
        "Tratamiento capilar",
        "Coloración / raíz",
        "Ver toda la agenda de Nadia",
    ]
    assert "Ver todos los servicios" not in quick_labels(body)
    assert_no_real_commitment_copy(body)


def test_change_service_after_nadia_schedule_clears_selection_and_cart_payload():
    availability_response = post_assistant(
        "Quiero reservar Corte profesional con Nadia Luisa el sábado a las 10:30",
        "nadia-change-service-session",
    )
    availability_body = availability_response.json()
    change_reply = find_quick_reply(availability_body, "Cambiar servicio")
    change_context = {
        **availability_body["context"],
        **change_reply["payload"],
    }

    response = post_assistant(
        change_reply["message"],
        "nadia-change-service-session",
        context=change_context,
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["flow_step"] == AssistantFlowStep.SERVICE_SELECTION.value
    assert body["cart_payload"] is None
    assert body["context"]["selected_professional"] == "Nadia Luisa"
    assert body["context"]["professional_id"] == "nadia_luisa"
    assert "selected_service" not in body["context"]
    assert body["context"]["requested_day"] == "sábado"
    assert body["context"]["requested_time"] == "10:30"
    assert body["context"]["service_change_mode"] is True
    assert "availability_status" not in body["context"]
    assert "cart_payload" not in body["context"]
    assert body["message"] == (
        "Corte profesional estaba seleccionado. Puedes elegir otro servicio "
        "de Nadia Luisa o revisar todos sus servicios."
    )
    assert quick_labels(body) == [
        "Corte profesional",
        "Brushing profesional",
        "Peinado social",
        "Tratamiento capilar",
        "Coloración / raíz",
        "Ver todos los servicios de Nadia",
    ]
    assert "Abonar 20% del servicio" not in quick_labels(body)
    assert find_quick_reply(body, "Ver todos los servicios de Nadia")["target"] == (
        "/services?professional=nadia_luisa"
    )
    assert_no_real_commitment_copy(body)


def test_service_change_mode_with_existing_time_asks_for_deposit():
    response = post_assistant(
        "Quiero reservar Corte profesional con Nadia Luisa",
        "nadia-service-change-abono-session",
        context={
            "intent": "booking",
            "selected_professional": "Nadia Luisa",
            "professional_id": "nadia_luisa",
            "professional_role": "Estilista profesional",
            "requested_day": "sábado",
            "requested_time": "10:30",
            "service_change_mode": True,
            "previous_service": "Brushing profesional",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["flow_step"] == AssistantFlowStep.AVAILABILITY_CHECK.value
    assert body["context"]["selected_professional"] == "Nadia Luisa"
    assert body["context"]["selected_service"] == "Corte profesional"
    assert body["context"]["requested_day"] == "sábado"
    assert body["context"]["requested_time"] == "10:30"
    assert body["cart_payload"]["service_label"] == "Corte profesional"
    assert body["cart_payload"]["deposit_percentage"] == 20
    assert body["cart_payload"]["remaining_percentage"] == 80
    assert body["cart_payload"]["schedule_status"] == "pending_confirmation"
    assert body["cart_payload"]["payment_status"] == "deposit_pending"
    assert body["message"] == (
        "Perfecto. Cambié el servicio a Corte profesional con Nadia Luisa "
        "para el sábado a las 10:30. ¿Quieres avanzar con el abono del 20%?"
    )
    assert quick_labels(body) == [
        "Abonar 20% del servicio",
        "Ver todos los servicios de Nadia",
        "Ver toda la agenda de Nadia",
    ]
    assert find_quick_reply(body, "Abonar 20% del servicio")["target"] == "/cart"
    assert find_quick_reply(body, "Abonar 20% del servicio")["payload"]["cart_payload"][
        "confirmation_status"
    ] == "not_confirmed"
    assert_pending_notice_not_duplicated(body)
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def test_maria_featured_services_show_clean_recommended_services():
    response = post_assistant("María Ignacia", "maria-featured-session")

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert "María Ignacia atiende cosmetología" in body["message"]
    assert quick_labels(body) == [
        "Limpieza facial",
        "Perfilado de cejas",
        "Laminado de cejas",
        "Hidratación facial",
        "Maquillaje",
        "Peinados femeninos",
        "Brushing",
        "Tratamiento capilar",
        "Ver todos los servicios de María Ignacia",
        "Volver a iniciar",
    ]
    assert "Ondas / brushing" not in quick_labels(body)
    assert "Ondas/ brushing" not in quick_labels(body)
    assert "Maquillaje social" not in quick_labels(body)
    assert "Peinado social" not in quick_labels(body)
    assert "Diagnóstico facial" not in quick_labels(body)
    assert "Preparación evento" not in quick_labels(body)
    assert "Ver más servicios de María" not in quick_labels(body)
    assert "Agendar ahora" not in quick_labels(body)
    assert find_quick_reply(
        body,
        "Ver todos los servicios de María Ignacia",
    )["target"] == "/services?professional=maria_ignacia"
    assert_no_real_commitment_copy(body)


def test_maria_more_services_returns_secondary_services():
    response = post_assistant(
        "Quiero ver más servicios de María Ignacia",
        "maria-more-services-session",
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert quick_labels(body) == [
        "Peinados femeninos",
        "Brushing",
        "Tratamiento capilar",
        "Ver todos los servicios de María Ignacia",
        "Volver a iniciar",
    ]
    assert "Ondas / brushing" not in quick_labels(body)
    assert "Maquillaje social" not in quick_labels(body)
    assert "Peinado social" not in quick_labels(body)
    assert "Diagnóstico facial" not in quick_labels(body)
    assert "Preparación evento" not in quick_labels(body)
    assert "Agendar ahora" not in quick_labels(body)
    assert find_quick_reply(
        body,
        "Ver todos los servicios de María Ignacia",
    )["target"] == "/services?professional=maria_ignacia"
    assert_no_real_commitment_copy(body)


def test_all_services_reply_targets_services_with_commercial_options():
    response = post_assistant("Todos los servicios", "all-services-session")

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["message"] == (
        "De las dos profesionales que atienden en el salón de belleza, "
        "¿qué servicios deseas revisar?"
    )
    assert quick_labels(body) == [
        "Nadia Luisa",
        "Maria Ignacia",
        "Volver a iniciar",
    ]
    assert find_quick_reply(body, "Nadia Luisa")["target"] == (
        "/services?professional=nadia_luisa"
    )
    assert find_quick_reply(body, "Maria Ignacia")["target"] == (
        "/services?professional=maria_ignacia"
    )
    assert find_quick_reply(body, "Volver a iniciar")["payload"]["reason"] == (
        "assistant_restart"
    )
    assert "Ver todos los servicios" not in quick_labels(body)
    assert "Servicios de Nadia" not in quick_labels(body)
    assert "Servicios de Maria" not in quick_labels(body)
    assert "Reservar hora" not in quick_labels(body)
    assert "Ver productos" not in quick_labels(body)
    assert_no_real_commitment_copy(body)


def test_maria_limpieza_facial_selection_moves_to_deposit_without_relisting():
    response = post_assistant(
        "Quiero reservar Limpieza facial con María Ignacia",
        "selected-service-session",
    )

    assert response.status_code == 200
    body = response.json()

    assert {
        "Limpieza facial",
        "Perfilado de cejas",
        "Laminado de cejas",
        "Hidratación facial",
        "Diagnóstico facial",
        "Maquillaje",
        "Peinados femeninos",
        "Brushing",
        "Tratamiento capilar",
        "Preparación evento",
    }.isdisjoint(quick_labels(body))
    assert_service_selection_deposit_response(
        body,
        "Limpieza facial",
        "María Ignacia",
        "maria_ignacia",
        "Cosmetóloga",
    )


def test_maria_second_service_offers_multi_service_options_without_relisting():
    first_response = post_assistant(
        "Quiero reservar Limpieza facial con María Ignacia",
        "maria-multi-service-session",
    )
    first_body = first_response.json()
    other_services_reply = find_quick_reply(
        first_body,
        "Ver todos los servicios de María Ignacia",
    )
    services_response = post_assistant(
        other_services_reply["message"],
        "maria-multi-service-session",
        context={**first_body["context"], **other_services_reply["payload"]},
    )
    services_body = services_response.json()

    assert services_body["context"]["selected_professional"] == "María Ignacia"
    assert services_body["context"]["professional_id"] == "maria_ignacia"
    assert services_body["context"]["professional_role"] == "Cosmetóloga"
    assert services_body["context"]["previous_service"] == "Limpieza facial"
    assert services_body["context"]["selected_service"] == "Limpieza facial"
    assert (
        services_body["context"]["service_selection_mode"]
        == "selecting_additional_service"
    )
    assert services_body["context"]["deposit_required"] is True
    assert services_body["context"]["deposit_percentage"] == 20
    assert quick_labels(services_body) == [
        "Limpieza facial",
        "Perfilado de cejas",
        "Laminado de cejas",
        "Hidratación facial",
        "Maquillaje",
        "Peinados femeninos",
        "Brushing",
        "Tratamiento capilar",
        "Ver todos los servicios de María Ignacia",
        "Volver a iniciar",
    ]
    assert "Diagnóstico facial" not in quick_labels(services_body)
    assert "Maquillaje social" not in quick_labels(services_body)
    assert "Peinado social" not in quick_labels(services_body)
    assert "Preparación evento" not in quick_labels(services_body)

    brushing_reply = find_quick_reply(services_body, "Brushing")

    response = post_assistant(
        brushing_reply["message"],
        "maria-multi-service-session",
        context=brushing_reply["payload"],
    )

    assert response.status_code == 200
    body = response.json()
    labels = quick_labels(body)

    assert body["message"] == (
        "Ya tenías seleccionado Limpieza facial. Ahora elegiste "
        "Brushing como servicio adicional. ¿Quieres preparar su abono "
        "o continuar solo con Limpieza facial?"
    )
    assert labels == [
        "Abonar 20% de Limpieza facial",
        "Abonar 20% de Brushing",
        "Descartar Brushing",
        "Volver a iniciar",
    ]
    assert "Agregar Limpieza facial al carrito" not in labels
    assert "Descartar Limpieza facial" not in labels
    assert {
        "Limpieza facial",
        "Perfilado de cejas",
        "Laminado de cejas",
        "Hidratación facial",
        "Diagnóstico facial",
        "Maquillaje",
        "Peinados femeninos",
        "Brushing",
        "Tratamiento capilar",
        "Preparación evento",
    }.isdisjoint(labels)
    assert body["cart_payload"] is None
    assert body["context"]["previous_service"] == "Limpieza facial"
    assert body["context"]["primary_service"] == "Limpieza facial"
    assert body["context"]["additional_service_candidate"] == "Brushing"
    assert body["context"]["selected_service"] == "Limpieza facial"
    assert (
        body["context"]["service_selection_mode"]
        == "selecting_additional_service"
    )
    assert body["context"]["multi_service_decision_mode"] is True
    assert body["redirect_target"] is None
    assert body["cart_payload"] is None
    assert find_quick_reply(
        body,
        "Abonar 20% de Limpieza facial",
    )["target"] is None
    assert find_quick_reply(body, "Abonar 20% de Brushing")["target"] is None
    assert_no_real_commitment_copy(body)


def test_maria_second_service_options_work_for_any_recommended_service():
    response = post_assistant(
        "Hidratación facial",
        "maria-any-second-service-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "service_selection_mode": True,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == (
        "Ya tenías seleccionado Limpieza facial. Ahora elegiste "
        "Hidratación facial como servicio adicional. ¿Quieres preparar su "
        "abono o continuar solo con Limpieza facial?"
    )
    assert quick_labels(body) == [
        "Abonar 20% de Limpieza facial",
        "Abonar 20% de Hidratación facial",
        "Descartar Hidratación facial",
        "Volver a iniciar",
    ]
    assert body["context"]["primary_service"] == "Limpieza facial"
    assert body["context"]["additional_service_candidate"] == "Hidratación facial"
    assert body["context"]["selected_service"] == "Limpieza facial"
    assert body["cart_payload"] is None
    assert body["redirect_target"] is None
    assert_no_real_commitment_copy(body)


def test_maria_second_service_options_work_for_another_primary_service():
    response = post_assistant(
        "Tratamiento capilar",
        "maria-any-primary-service-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "primary_service": "Perfilado de cejas",
            "selected_service": "Perfilado de cejas",
            "service_selection_mode": True,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == (
        "Ya tenías seleccionado Perfilado de cejas. Ahora elegiste "
        "Tratamiento capilar como servicio adicional. ¿Quieres preparar su "
        "abono o continuar solo con Perfilado de cejas?"
    )
    assert quick_labels(body) == [
        "Abonar 20% de Perfilado de cejas",
        "Abonar 20% de Tratamiento capilar",
        "Descartar Tratamiento capilar",
        "Volver a iniciar",
    ]
    assert body["context"]["primary_service"] == "Perfilado de cejas"
    assert body["context"]["additional_service_candidate"] == "Tratamiento capilar"
    assert body["context"]["selected_service"] == "Perfilado de cejas"
    assert body["cart_payload"] is None
    assert body["redirect_target"] is None
    assert_no_real_commitment_copy(body)


def test_add_additional_maria_service_to_cart_does_not_reoffer_add_button():
    response = post_assistant(
        "Abonar 20% de Brushing",
        "maria-add-additional-service-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "additional_service_candidate": "Brushing",
            "multi_service_decision_mode": True,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )

    assert response.status_code == 200
    body = response.json()
    labels = quick_labels(body)

    assert body["message"] == (
        "Preparé el abono del 20% de Brushing. Puedes revisar tu "
        "selección en el carrito, agregar más servicios o volver a "
        "iniciar."
    )
    assert labels == [
        "Ir a Carrito de compras",
        "Agregar más servicios",
        "Volver a iniciar",
    ]
    assert "Abonar 20% de Brushing" not in labels
    assert "Descartar Brushing" not in labels
    assert body["cart_payload"]["cart_count"] == 1
    assert body["cart_payload"]["items"][0]["service_label"] == "Brushing"
    assert body["context"]["primary_service"] == "Limpieza facial"
    assert body["context"]["selected_service"] == "Limpieza facial"
    assert "additional_service_candidate" not in body["context"]
    assert "multi_service_decision_mode" not in body["context"]
    assert body["context"]["cart_count"] == 1
    assert body["context"]["cart_items"] == ["Brushing"]
    assert body["context"]["cart_payload"]["cart_count"] == 1
    assert body["redirect_target"] is None
    assert find_quick_reply(body, "Ir a Carrito de compras")["target"] == "/cart"
    assert_no_real_commitment_copy(body)


def test_maria_multi_service_flow_prepares_brushing_then_checkout_locks():
    first_response = post_assistant(
        "Quiero reservar Limpieza facial con María Ignacia",
        "maria-multi-service-flow-session",
    )
    first_body = first_response.json()
    other_services_reply = find_quick_reply(
        first_body,
        "Ver todos los servicios de María Ignacia",
    )
    services_response = post_assistant(
        other_services_reply["message"],
        "maria-multi-service-flow-session",
        context={**first_body["context"], **other_services_reply["payload"]},
    )
    services_body = services_response.json()
    brushing_reply = find_quick_reply(services_body, "Brushing")

    brushing_selection_response = post_assistant(
        brushing_reply["message"],
        "maria-multi-service-flow-session",
        context=brushing_reply["payload"],
    )
    brushing_selection_body = brushing_selection_response.json()
    brushing_preparation_reply = find_quick_reply(
        brushing_selection_body,
        "Abonar 20% de Brushing",
    )

    brushing_preparation_response = post_assistant(
        brushing_preparation_reply["message"],
        "maria-multi-service-flow-session",
        context={
            **brushing_selection_body["context"],
            **brushing_preparation_reply["payload"],
        },
    )
    brushing_preparation_body = brushing_preparation_response.json()
    cart_redirect_reply = find_quick_reply(
        brushing_preparation_body,
        "Ir a Carrito de compras",
    )

    final_response = post_assistant(
        cart_redirect_reply["message"],
        "maria-multi-service-flow-session",
        context={
            **brushing_preparation_body["context"],
            **cart_redirect_reply["payload"],
        },
    )
    final_body = final_response.json()

    assert brushing_selection_response.status_code == 200
    assert brushing_preparation_response.status_code == 200
    assert final_response.status_code == 200

    assert quick_labels(brushing_selection_body) == [
        "Abonar 20% de Limpieza facial",
        "Abonar 20% de Brushing",
        "Descartar Brushing",
        "Volver a iniciar",
    ]
    assert "Ver todos los servicios de María Ignacia" not in quick_labels(
        brushing_selection_body
    )
    assert find_quick_reply(
        brushing_selection_body,
        "Abonar 20% de Brushing",
    )["target"] is None
    assert brushing_selection_body["cart_payload"] is None

    assert quick_labels(brushing_preparation_body) == [
        "Ir a Carrito de compras",
        "Agregar más servicios",
        "Volver a iniciar",
    ]
    assert brushing_preparation_body["cart_payload"]["cart_count"] == 1
    assert brushing_preparation_body["context"]["cart_count"] == 1
    assert brushing_preparation_body["context"]["cart_items"] == ["Brushing"]
    assert find_quick_reply(
        brushing_preparation_body,
        "Ir a Carrito de compras",
    )["target"] == "/cart"

    assert final_body["message"] == (
        "Perfecto. Te llevé al carrito para revisar el detalle de tu "
        "selección. La hora quedará pendiente hasta confirmación del "
        "salón. Importante: si presionas Volver a iniciar, se "
        "reiniciará el chat y se eliminarán las selecciones actuales "
        "del carrito. Tendrás que comenzar el proceso nuevamente."
    )
    assert final_body["cart_payload"]["cart_count"] == 1
    assert final_body["context"]["cart_count"] == 1
    assert final_body["context"]["checkout_ready"] is True
    assert final_body["context"]["conversation_locked"] is True
    assert final_body["context"]["cart_redirected"] is True
    assert final_body["context"]["cart_items"] == [
        "Brushing",
    ]
    assert quick_labels(final_body) == ["Volver a iniciar"]
    assert "Ir a Carrito de compras" not in quick_labels(final_body)
    assert "Abonar 20% de Brushing" not in quick_labels(final_body)
    assert "Abonar 20% del servicio" not in quick_labels(final_body)
    assert "Abonar 20% de Limpieza facial" not in quick_labels(final_body)
    assert "Ver todos los servicios de María Ignacia" not in quick_labels(final_body)
    assert "Agregar más servicios" not in quick_labels(final_body)
    assert final_body["redirect_target"] is None
    assert_no_real_commitment_copy(brushing_selection_body)
    assert_no_real_commitment_copy(brushing_preparation_body)
    assert_no_real_commitment_copy(final_body)


def test_add_more_maria_services_preserves_cart_items_for_next_candidate():
    more_response = post_assistant(
        "Agregar más servicios",
        "maria-add-more-services-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "cart_items": ["Brushing"],
            "cart_count": 1,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )

    assert more_response.status_code == 200
    more_body = more_response.json()

    assert more_body["context"]["primary_service"] == "Limpieza facial"
    assert more_body["context"]["selected_service"] == "Limpieza facial"
    assert more_body["context"]["cart_items"] == ["Brushing"]
    assert more_body["context"]["cart_count"] == 1
    assert quick_labels(more_body) == [
        "Limpieza facial",
        "Perfilado de cejas",
        "Laminado de cejas",
        "Hidratación facial",
        "Maquillaje",
        "Peinados femeninos",
        "Brushing",
        "Tratamiento capilar",
        "Ver todos los servicios de María Ignacia",
        "Volver a iniciar",
    ]

    response = post_assistant(
        "Maquillaje",
        "maria-add-more-services-session",
        context={
            **more_body["context"],
            "service_selection_mode": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    labels = quick_labels(body)

    assert labels == [
        "Abonar 20% de Limpieza facial",
        "Abonar 20% de Maquillaje",
        "Descartar Maquillaje",
        "Volver a iniciar",
    ]
    assert body["context"]["primary_service"] == "Limpieza facial"
    assert body["context"]["selected_service"] == "Limpieza facial"
    assert body["context"]["additional_service_candidate"] == "Maquillaje"
    assert body["context"]["cart_items"] == ["Brushing"]
    assert body["context"]["cart_count"] == 1
    assert body["cart_payload"] is None
    assert body["redirect_target"] is None
    assert_no_real_commitment_copy(body)


def test_cart_redirect_after_adding_additional_service_returns_terminal_message():
    response = post_assistant(
        "Ir a Carrito de compras",
        "maria-pay-added-additional-service-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "cart_items": ["Brushing"],
            "cart_count": 1,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )

    assert response.status_code == 200
    body = response.json()
    cart_payload = body["cart_payload"]

    assert body["message"] == (
        "Perfecto. Te llevé al carrito para revisar el detalle de tu "
        "selección. La hora quedará pendiente hasta confirmación del "
        "salón. Importante: si presionas Volver a iniciar, se "
        "reiniciará el chat y se eliminarán las selecciones actuales "
        "del carrito. Tendrás que comenzar el proceso nuevamente."
    )
    assert body["redirect_target"] is None
    assert cart_payload["deposit_percentage"] == 20
    assert cart_payload["remaining_percentage"] == 80
    assert cart_payload["amount_status"] == "pending_final_price"
    assert cart_payload["payment_status"] == "deposit_pending"
    assert cart_payload["confirmation_status"] == "not_confirmed"
    assert cart_payload["schedule_status"] == "pending_selection"
    assert cart_payload["total_items"] == 1
    assert cart_payload["cart_count"] == 1
    assert len(cart_payload["items"]) == 1
    assert [item["service_label"] for item in cart_payload["items"]] == [
        "Brushing",
    ]
    assert all(
        item["amount_status"] == "pending_final_price"
        for item in cart_payload["items"]
    )
    assert all("deposit_amount" not in item for item in cart_payload["items"])
    assert all("remaining_amount" not in item for item in cart_payload["items"])
    assert body["context"]["checkout_ready"] is True
    assert body["context"]["conversation_locked"] is True
    assert body["context"]["cart_redirected"] is True
    assert body["context"]["cart_count"] == 1
    assert body["context"]["cart_items"] == ["Brushing"]
    assert quick_labels(body) == ["Volver a iniciar"]
    assert "Ir a Carrito de compras" not in quick_labels(body)
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def test_pay_primary_maria_service_without_additional_uses_single_item_cart_payload():
    response = post_assistant(
        "Abonar 20% de Limpieza facial",
        "maria-pay-primary-service-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )

    assert response.status_code == 200
    body = response.json()
    cart_payload = body["cart_payload"]

    assert body["redirect_target"] == "/cart"
    assert cart_payload["deposit_percentage"] == 20
    assert cart_payload["remaining_percentage"] == 80
    assert cart_payload["amount_status"] == "pending_final_price"
    assert cart_payload["payment_status"] == "deposit_pending"
    assert cart_payload["confirmation_status"] == "not_confirmed"
    assert cart_payload["total_items"] == 1
    assert cart_payload["cart_count"] == 1
    assert len(cart_payload["items"]) == 1
    assert cart_payload["items"][0]["service_label"] == "Limpieza facial"
    assert cart_payload["items"][0]["amount_status"] == "pending_final_price"
    assert "service_price" not in cart_payload
    assert "deposit_amount" not in cart_payload
    assert "remaining_amount" not in cart_payload
    assert "deposit_amount" not in cart_payload["items"][0]
    assert "remaining_amount" not in cart_payload["items"][0]
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def test_discard_additional_maria_service_keeps_primary_service():
    response = post_assistant(
        "Descartar Brushing",
        "maria-discard-additional-service-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "additional_service_candidate": "Brushing",
            "multi_service_decision_mode": True,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == (
        "Perfecto. Descarté Brushing y mantuve Limpieza facial como servicio "
        "principal."
    )
    assert quick_labels(body) == [
        "Agregar más servicios",
        "Volver a iniciar",
    ]
    assert body["context"]["primary_service"] == "Limpieza facial"
    assert body["context"]["selected_service"] == "Limpieza facial"
    assert "additional_service_candidate" not in body["context"]
    assert "cart_items" not in body["context"]
    assert "cart_count" not in body["context"]
    assert "multi_service_decision_mode" not in body["context"]
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def test_maria_perfilado_selection_moves_to_deposit_without_relisting():
    response = post_assistant(
        "Quiero reservar Perfilado de cejas con María Ignacia",
        "maria-perfilado-selection-session",
    )

    assert response.status_code == 200
    body = response.json()

    assert "Limpieza facial" not in quick_labels(body)
    assert "Perfilado de cejas" not in quick_labels(body)
    assert_service_selection_deposit_response(
        body,
        "Perfilado de cejas",
        "María Ignacia",
        "maria_ignacia",
        "Cosmetóloga",
    )


def test_maria_peinados_femeninos_selection_moves_to_deposit_without_relisting():
    response = post_assistant(
        "Quiero reservar Peinados femeninos con María Ignacia",
        "maria-peinado-selection-session",
    )

    assert response.status_code == 200
    body = response.json()

    assert "Peinado social" not in quick_labels(body)
    assert "Maquillaje social" not in quick_labels(body)
    assert_service_selection_deposit_response(
        body,
        "Peinados femeninos",
        "María Ignacia",
        "maria_ignacia",
        "Cosmetóloga",
    )


def test_maria_service_change_mode_with_existing_time_asks_for_deposit():
    response = post_assistant(
        "Quiero reservar Perfilado de cejas con María Ignacia",
        "maria-service-change-abono-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "previous_service": "Limpieza facial",
            "requested_day": "miércoles",
            "requested_time": "16:00",
            "service_change_mode": True,
            "deposit_required": True,
            "deposit_percentage": 20,
            "cart_payload": {
                "type": "booking_deposit",
                "status": "pending_deposit",
                "deposit_percentage": 20,
                "remaining_percentage": 80,
                "service_label": "Limpieza facial",
                "professional_label": "María Ignacia",
                "requested_day": "miércoles",
                "requested_time": "16:00",
                "confirmation_status": "not_confirmed",
                "payment_status": "deposit_pending",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    labels = quick_labels(body)
    cart_payload = body["cart_payload"]
    abono_reply = find_quick_reply(body, "Abonar 20% del servicio")

    assert body["flow_step"] == AssistantFlowStep.AVAILABILITY_CHECK.value
    assert body["context"]["selected_professional"] == "María Ignacia"
    assert body["context"]["professional_id"] == "maria_ignacia"
    assert body["context"]["professional_role"] == "Cosmetóloga"
    assert body["context"]["previous_service"] == "Limpieza facial"
    assert body["context"]["selected_service"] == "Perfilado de cejas"
    assert body["context"]["requested_day"] == "miércoles"
    assert body["context"]["requested_time"] == "16:00"
    assert body["context"]["service_change_mode"] is True
    assert body["message"] == (
        "Perfecto. Cambié el servicio a Perfilado de cejas con María Ignacia "
        "para el miércoles a las 16:00. ¿Quieres avanzar con el abono del 20%?"
    )
    assert labels == [
        "Abonar 20% del servicio",
        "Ver todos los servicios de María Ignacia",
        "Volver a iniciar",
    ]
    assert {
        "Limpieza facial",
        "Perfilado de cejas",
        "Maquillaje",
        "Peinados femeninos",
        "Tratamiento capilar",
    }.isdisjoint(labels)
    assert abono_reply["target"] == "/cart"
    assert abono_reply["payload"]["cart_payload"]["selected_professional"] == (
        "María Ignacia"
    )
    assert abono_reply["payload"]["cart_payload"]["selected_service"] == (
        "Perfilado de cejas"
    )
    assert cart_payload["deposit_percentage"] == 20
    assert cart_payload["remaining_percentage"] == 80
    assert cart_payload["schedule_status"] == "pending_confirmation"
    assert cart_payload["confirmation_status"] == "not_confirmed"
    assert cart_payload["payment_status"] == "deposit_pending"
    assert_pending_notice_not_duplicated(body)
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def test_restart_reply_resets_assistant_booking_context_without_navigation():
    response = post_assistant(
        "Volver a iniciar",
        "assistant-restart-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "selected_service": "Perfilado de cejas",
            "previous_service": "Limpieza facial",
            "primary_service": "Limpieza facial",
            "additional_service_candidate": "Brushing",
            "cart_items": ["Brushing"],
            "cart_count": 1,
            "requested_day": "miércoles",
            "requested_time": "16:00",
            "multi_service_decision_mode": True,
            "service_change_mode": True,
            "service_selection_mode": True,
            "availability_status": "pending_schedule_selection",
            "cart_payload": {
                "type": "booking_deposit",
                "status": "pending_deposit",
                "deposit_percentage": 20,
                "remaining_percentage": 80,
                "service_label": "Perfilado de cejas",
                "professional_label": "María Ignacia",
                "requested_day": "miércoles",
                "requested_time": "16:00",
                "confirmation_status": "not_confirmed",
                "payment_status": "deposit_pending",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["redirect_target"] is None
    assert body["cart_payload"] is None
    assert body["message"] == (
        "Hola, soy la asistente virtual de Always Beautiful. Puedo ayudarte a "
        "reservar una hora, revisar servicios o ver productos. ¿Qué "
        "quieres hacer?"
    )
    assert quick_labels(body) == ["Reservar hora", "Ver servicios", "Ver productos"]
    assert find_quick_reply(body, "Reservar hora")["target"] is None
    assert find_quick_reply(body, "Ver servicios")["target"] == "/services"
    assert find_quick_reply(body, "Ver productos")["target"] == "/products"
    assert "selected_professional" not in body["context"]
    assert "selected_service" not in body["context"]
    assert "previous_service" not in body["context"]
    assert "primary_service" not in body["context"]
    assert "additional_service_candidate" not in body["context"]
    assert "requested_day" not in body["context"]
    assert "requested_time" not in body["context"]
    assert "cart_payload" not in body["context"]
    assert "cart_items" not in body["context"]
    assert "cart_count" not in body["context"]
    assert "multi_service_decision_mode" not in body["context"]
    assert "service_change_mode" not in body["context"]
    assert "service_selection_mode" not in body["context"]
    assert "availability_status" not in body["context"]
    assert_no_real_commitment_copy(body)


def test_products_after_restart_does_not_keep_maria_booking_context():
    restart_response = post_assistant(
        "Volver a iniciar",
        "assistant-restart-products-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "previous_service": "Limpieza facial",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "additional_service_candidate": "Hidratación facial",
            "cart_items": ["Brushing"],
            "cart_count": 1,
            "cart_payload": {"type": "booking_deposit"},
            "multi_service_decision_mode": True,
            "service_selection_mode": True,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )
    restart_body = restart_response.json()

    response = post_assistant(
        "Ver productos",
        "assistant-restart-products-session",
        context=restart_body["context"],
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.PRODUCT_RECOMMENDATION.value
    assert body["flow_step"] == AssistantFlowStep.PRODUCT_SELECTION.value
    assert body["redirect_target"] is None
    assert body["cart_payload"] is None
    assert "selected_professional" not in body["context"]
    assert "selected_service" not in body["context"]
    assert "previous_service" not in body["context"]
    assert "primary_service" not in body["context"]
    assert "additional_service_candidate" not in body["context"]
    assert "cart_payload" not in body["context"]
    assert "cart_items" not in body["context"]
    assert "cart_count" not in body["context"]
    assert "multi_service_decision_mode" not in body["context"]
    assert "Limpieza facial" not in quick_labels(body)
    assert "Hidratación facial" not in quick_labels(body)
    assert find_quick_reply(body, "Ver productos")["target"] == "/products"
    assert_no_real_commitment_copy(body)


def test_booking_after_restart_asks_professional_from_scratch():
    restart_response = post_assistant(
        "Volver a iniciar",
        "assistant-restart-booking-session",
        context={
            "intent": "booking",
            "selected_professional": "María Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetóloga",
            "previous_service": "Limpieza facial",
            "primary_service": "Limpieza facial",
            "selected_service": "Limpieza facial",
            "additional_service_candidate": "Hidratación facial",
            "cart_items": ["Brushing"],
            "cart_count": 1,
            "cart_payload": {"type": "booking_deposit"},
            "multi_service_decision_mode": True,
            "service_selection_mode": True,
            "deposit_required": True,
            "deposit_percentage": 20,
        },
    )
    restart_body = restart_response.json()

    response = post_assistant(
        "Reservar hora",
        "assistant-restart-booking-session",
        context=restart_body["context"],
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["flow_step"] == AssistantFlowStep.PROFESSIONAL_SELECTION.value
    assert "selected_professional" not in body["context"]
    assert "selected_service" not in body["context"]
    assert "previous_service" not in body["context"]
    assert "primary_service" not in body["context"]
    assert "additional_service_candidate" not in body["context"]
    assert "cart_payload" not in body["context"]
    assert "cart_items" not in body["context"]
    assert "cart_count" not in body["context"]
    assert "multi_service_decision_mode" not in body["context"]
    assert quick_labels(body) == [
        "Nadia Luisa",
        "María Ignacia",
    ]
    assert "No estoy segura" not in quick_labels(body)
    assert_no_real_commitment_copy(body)


def test_assistant_cart_draft_is_cleared_on_inactivity_expiration_contract():
    source = (
        REPO_ROOT / "web/src/components/shared/AssistantChatWidget.jsx"
    ).read_text()
    close_timer_section = source.split("const closeTimer = globalThis.setTimeout", 1)[
        1
    ]

    assert "alwaysBeautifulAssistantCartDraft" in source
    assert "always-beautiful:assistant-cart-handoff" in source
    assert "storage.removeItem(ASSISTANT_CART_DRAFT_STORAGE_KEY)" in source
    assert "storage.removeItem(ASSISTANT_CART_HANDOFF_STORAGE_KEY)" in source
    assert "clearAssistantFlowStorage();" in close_timer_section
    assert (
        "setConversationContext(INITIAL_ASSISTANT_MESSAGE.context)"
        in close_timer_section
    )


def test_assistant_message_list_auto_scroll_contract():
    source = (
        REPO_ROOT / "web/src/components/shared/AssistantMessageList.jsx"
    ).read_text()

    assert "useEffect" in source
    assert "useRef" in source
    assert "scrollIntoView" in source
    assert "messages.length" in source


def test_assistant_chat_widget_collapses_history_after_cart_redirect_contract():
    source = (
        REPO_ROOT / "web/src/components/shared/AssistantChatWidget.jsx"
    ).read_text()

    assert "response.context?.cart_redirected" in source
    assert "setMessages([assistantMessage]);" in source
    assert "setConversationLocked(true);" in source


def test_public_header_cart_badge_is_hidden_without_assistant_cart_count():
    source = (REPO_ROOT / "web/src/components/shared/PublicHeader.jsx").read_text()

    assert "alwaysBeautifulAssistantCartDraft" in source
    assert "cart_items" in source
    assert "payloadItems.length" in source
    assert "draftItems.length" in source
    assert "assistantCartCount > 0" in source
    assert "public-header__cart-count" in source


def test_service_professional_day_and_time_returns_tentative_availability():
    response = post_assistant(
        "Quiero limpieza facial con María Ignacia el miércoles a las 15:00",
        "tentative-availability-session",
    )

    assert response.status_code == 200
    body = response.json()
    quick_reply = find_quick_reply(body, "Abonar 20% del servicio")

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["flow_step"] == AssistantFlowStep.AVAILABILITY_CHECK.value
    assert "disponible de forma tentativa" in body["message"]
    assert body["redirect_target"] is None
    assert body["cart_payload"]["type"] == "booking_deposit"
    assert body["cart_payload"]["deposit_percentage"] == 20
    assert body["cart_payload"]["remaining_percentage"] == 80
    assert body["cart_payload"]["schedule_status"] == "pending_confirmation"
    assert body["cart_payload"]["payment_status"] == "deposit_pending"
    assert quick_reply["action_type"] == "cart_handoff"
    assert quick_reply["target"] == "/cart"
    assert quick_reply["payload"]["cart_payload"]["confirmation_status"] == (
        "not_confirmed"
    )
    assert_pending_notice_not_duplicated(body)
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def test_incomplete_deposit_handoff_targets_booking_without_cart_payload():
    response = post_assistant(
        "Continuar y pagar abono del 20%.",
        "incomplete-deposit-session",
    )

    assert response.status_code == 200
    body = response.json()
    quick_reply = find_quick_reply(body, "Ir a reservar")

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["redirect_target"] is None
    assert body["cart_payload"] is None
    assert "Abonar 20% del servicio" not in quick_labels(body)
    assert quick_reply["action_type"] == "navigate"
    assert quick_reply["target"] == "/booking"
    assert quick_reply["payload"]["reason"] == "missing_booking_deposit_data"
    assert_no_real_commitment_copy(body)


def test_complete_deposit_handoff_returns_cart_contract():
    response = post_assistant(
        (
            "Quiero reservar una limpieza facial con María Ignacia el miércoles "
            "a las 15:00. Continuar y pagar abono del 20%."
        ),
        "complete-deposit-session",
    )

    assert response.status_code == 200
    body = response.json()
    cart_payload = body["cart_payload"]
    quick_reply = find_quick_reply(body, "Abonar 20% del servicio")

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert body["redirect_target"] == "/cart"
    assert cart_payload["type"] == "booking_deposit"
    assert cart_payload["status"] == "pending_deposit"
    assert cart_payload["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert cart_payload["remaining_percentage"] == 80
    assert cart_payload["professional_label"] == "María Ignacia"
    assert cart_payload["service_label"] == "Limpieza facial"
    assert cart_payload["requested_day"] == "miércoles"
    assert cart_payload["requested_time"] == "15:00"
    assert cart_payload["schedule_status"] == "pending_confirmation"
    assert cart_payload["confirmation_status"] == "not_confirmed"
    assert cart_payload["payment_status"] == "deposit_pending"
    assert quick_reply["action_type"] == "cart_handoff"
    assert quick_reply["target"] == "/cart"
    assert quick_reply["payload"]["reason"] == "booking_deposit_handoff"
    assert_deposit_terms_notice_not_duplicated(body)
    assert_no_real_commitment_copy(body)


def test_nadia_cosmetology_block_preserves_service_day_and_time_for_maria():
    blocked_response = post_assistant(
        "Quiero reservar una limpieza facial con Nadia Luisa el miércoles a las 15:00.",
        "nadia-to-maria-session",
    )

    assert blocked_response.status_code == 200
    blocked_body = blocked_response.json()
    switch_reply = find_quick_reply(blocked_body, "Continuar con María")

    assert blocked_body["intent"] == AssistantIntent.BOOKING.value
    assert blocked_body["flow_step"] == AssistantFlowStep.PROFESSIONAL_SELECTION.value
    assert blocked_body["redirect_target"] is None
    assert blocked_body["cart_payload"] is None
    assert blocked_body["message"] == (
        "Nadia Luisa no realiza servicios de cosmetología. Para ese servicio "
        "puede atenderte María Ignacia."
    )
    assert quick_labels(blocked_body) == [
        "Continuar con María",
        "Cambiar servicio",
        "Ver todos los servicios",
    ]
    assert find_quick_reply(blocked_body, "Ver todos los servicios")["target"] == (
        "/services"
    )

    preserved_context = switch_reply["payload"]
    assert preserved_context["context"]["selected_professional"] == "María Ignacia"
    assert preserved_context["context"]["professional_id"] == "maria_ignacia"
    assert preserved_context["context"]["professional_role"] == "Cosmetóloga"

    continuation_response = post_assistant(
        switch_reply["message"],
        "nadia-to-maria-session",
        context=preserved_context,
    )

    assert continuation_response.status_code == 200
    continuation_body = continuation_response.json()

    assert continuation_body["flow_step"] == AssistantFlowStep.DEPOSIT_CONFIRMATION.value
    assert continuation_body["context"]["selected_professional"] == "María Ignacia"
    assert continuation_body["context"]["selected_service"] == "Limpieza facial"
    assert continuation_body["context"]["requested_day"] == "miércoles"
    assert continuation_body["context"]["requested_time"] == "15:00"
    assert "Abonar 20% del servicio" in quick_labels(continuation_body)
    assert continuation_body["cart_payload"]["schedule_status"] == (
        "pending_confirmation"
    )
    assert_no_real_commitment_copy(blocked_body)
    assert_no_real_commitment_copy(continuation_body)


def test_product_flow_still_works_without_booking_handoff():
    response = post_assistant(
        "Quiero comprar un producto para cuidar el cabello.",
        "product-session",
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.PRODUCT_RECOMMENDATION.value
    assert body["flow_step"] == AssistantFlowStep.PRODUCT_SELECTION.value
    assert body["requires_deposit"] is False
    assert body["deposit_percentage"] == 0
    assert body["redirect_target"] is None
    assert body["cart_payload"] is None
    assert_no_real_commitment_copy(body)


def test_assistant_detects_common_spanish_booking_variants():
    response = post_assistant("reservar ora", "booking-variant-session")

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == AssistantIntent.BOOKING.value
    assert quick_labels(body) == [
        "Nadia Luisa",
        "María Ignacia",
    ]
    assert "No estoy segura" not in quick_labels(body)
    assert_no_real_commitment_copy(body)


def test_assistant_chat_rejects_invalid_request():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "invalid-session",
            "channel": "web",
        },
    )

    assert response.status_code == 422
