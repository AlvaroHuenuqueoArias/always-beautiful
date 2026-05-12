from fastapi.testclient import TestClient

from app.assistant.policies import (
    BOOKING_DEPOSIT_PERCENTAGE,
    booking_deposit_required_notice,
)
from app.assistant.state import AssistantFlowStep, AssistantIntent
from app.main import app


client = TestClient(app)

FORBIDDEN_BOOKING_CONFIRMATION_COPY = (
    "reserva confirmada",
    "hora confirmada",
    "cita agendada",
)


def assert_no_confirmed_booking_copy(body):
    combined_text = (
        f"{body.get('message', '')} "
        f"{' '.join(body.get('next_actions', []))}"
    ).lower()

    for forbidden_copy in FORBIDDEN_BOOKING_CONFIRMATION_COPY:
        assert forbidden_copy not in combined_text


def test_assistant_health():
    response = client.get("/assistant/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "module": "assistant"}


def test_assistant_prepares_booking_conversion_intent_without_activating_it():
    assert AssistantIntent.BOOKING_CONVERSION.value == "booking_conversion"


def test_assistant_detects_booking_intent():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "booking-session",
            "message": "Quiero reservar una hora para un tratamiento facial",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "booking"
    assert "flow_step" in body
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert_no_confirmed_booking_copy(body)


def test_assistant_booking_day_moves_to_time_selection():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "booking-day-session",
            "message": "Quiero agendar el miércoles.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["flow_step"] == AssistantFlowStep.TIME_SELECTION.value
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert (
        "hora prefieres" in body["message"]
        or "Indicar una hora." in body["next_actions"]
    )
    assert_no_confirmed_booking_copy(body)


def test_assistant_day_and_time_runs_read_only_availability_check():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "booking-availability-session",
            "message": "Quiero agendar el miércoles a las 15:00.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["flow_step"] == AssistantFlowStep.AVAILABILITY_CHECK.value
    assert "disponible de forma tentativa" in body["message"]
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert "Continuar y pagar abono del 20%." in body["next_actions"]
    assert_no_confirmed_booking_copy(body)


def test_assistant_unavailable_time_suggests_alternatives():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "booking-unavailable-session",
            "message": "Quiero agendar el miércoles a las 13:00.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["flow_step"] == AssistantFlowStep.AVAILABILITY_CHECK.value
    assert "no aparece disponible" in body["message"]
    assert "Probar 16:00." in body["next_actions"]
    assert "Probar 17:00." in body["next_actions"]
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert_no_confirmed_booking_copy(body)


def test_assistant_detects_product_purchase_intent():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "product-session",
            "message": "Necesito una recomendación de shampoo para comprar",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "product_recommendation"
    assert body["flow_step"] == AssistantFlowStep.PRODUCT_SELECTION.value
    assert body["requires_deposit"] is False
    assert body["deposit_percentage"] == 0
    assert "carrito" in " ".join(body["next_actions"]).lower()
    assert_no_confirmed_booking_copy(body)


def test_assistant_prioritizes_product_purchase_over_treatment_context():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "product-treatment-session",
            "message": (
                "Quiero comprar un producto para cuidar el cabello después "
                "de un tratamiento."
            ),
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "product_recommendation"
    assert body["flow_step"] == AssistantFlowStep.PRODUCT_SELECTION.value
    assert body["requires_deposit"] is False
    assert body["deposit_percentage"] == 0
    assert_no_confirmed_booking_copy(body)


def test_assistant_booking_response_includes_deposit_rule():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "deposit-session",
            "message": "Necesito agendar un servicio de estilismo",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    combined_text = f"{body['message']} {' '.join(body['next_actions'])}"

    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == 20
    assert "flow_step" in body
    assert "20%" in combined_text
    assert "desde la web" in combined_text
    assert_no_confirmed_booking_copy(body)


def test_assistant_blocks_cosmetology_with_nadia_luisa():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "cosmetology-nadia-session",
            "message": "Quiero reservar una limpieza facial con Nadia Luisa.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    combined_text = f"{body['message']} {' '.join(body['next_actions'])}"

    assert body["intent"] == "booking"
    assert body["flow_step"] == AssistantFlowStep.PROFESSIONAL_SELECTION.value
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert "Nadia Luisa no realiza servicios de cosmetología" in body["message"]
    assert "María Ignacia" in combined_text
    assert "Continuar con María Ignacia." in body["next_actions"]
    assert "Cambiar servicio." in body["next_actions"]
    assert "Elegir otra profesional." in body["next_actions"]
    assert_no_confirmed_booking_copy(body)


def test_assistant_blocks_cosmetology_with_nadia_luisa_before_availability():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "cosmetology-nadia-availability-session",
            "message": (
                "Quiero reservar una limpieza facial con Nadia Luisa el "
                "miércoles a las 15:00."
            ),
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["flow_step"] == AssistantFlowStep.PROFESSIONAL_SELECTION.value
    assert "Nadia Luisa no realiza servicios de cosmetología" in body["message"]
    assert "María Ignacia" in body["message"]
    assert "disponible" not in body["message"].lower()
    assert_no_confirmed_booking_copy(body)


def test_assistant_allows_cosmetology_with_maria_ignacia():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "cosmetology-maria-session",
            "message": "Quiero reservar una limpieza facial con María Ignacia.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert "no realiza servicios de cosmetología" not in body["message"]
    assert_no_confirmed_booking_copy(body)


def test_assistant_allows_cosmetology_with_maria_ignacia_availability_check():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "cosmetology-maria-availability-session",
            "message": (
                "Quiero reservar una limpieza facial con María Ignacia el "
                "miércoles a las 15:00."
            ),
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["flow_step"] == AssistantFlowStep.AVAILABILITY_CHECK.value
    assert "no realiza servicios de cosmetología" not in body["message"]
    assert "disponible de forma tentativa" in body["message"]
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert_no_confirmed_booking_copy(body)


def test_assistant_allows_styling_with_nadia_luisa():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "styling-nadia-session",
            "message": "Quiero reservar peinado con Nadia Luisa.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert "no realiza servicios de cosmetología" not in body["message"]
    assert_no_confirmed_booking_copy(body)


def test_assistant_allows_styling_with_maria_ignacia():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "styling-maria-session",
            "message": "Quiero reservar peinado con María Ignacia.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert "no realiza servicios de cosmetología" not in body["message"]
    assert_no_confirmed_booking_copy(body)


def test_assistant_rejects_booking_without_deposit_confirmation():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "deposit-avoidance-session",
            "message": "Agéndame una hora sin pagar el abono.",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["intent"] == "booking"
    assert body["flow_step"] == AssistantFlowStep.DEPOSIT_CONFIRMATION.value
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert booking_deposit_required_notice() in body["message"]
    assert_no_confirmed_booking_copy(body)


def test_assistant_cosmetologist_can_cover_styling():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "professional-session",
            "message": "Quiero reservar peinado y estilismo profesional",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    combined_text = f"{body['message']} {' '.join(body['next_actions'])}"

    assert body["intent"] == "booking"
    assert "flow_step" in body
    assert "Cosmetóloga" in combined_text
    assert "estilismo profesional" in combined_text
    assert_no_confirmed_booking_copy(body)


def test_assistant_chat_rejects_invalid_request():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "invalid-session",
            "channel": "web",
        },
    )

    assert response.status_code == 422
