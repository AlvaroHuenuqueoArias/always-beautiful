from fastapi.testclient import TestClient

from app.assistant.policies import (
    BOOKING_DEPOSIT_PERCENTAGE,
    booking_deposit_required_notice,
)
from app.main import app


client = TestClient(app)


def test_assistant_health():
    response = client.get("/assistant/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "module": "assistant"}


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
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE


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
    assert body["requires_deposit"] is False
    assert body["deposit_percentage"] == 0
    assert "carrito" in " ".join(body["next_actions"]).lower()


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
    assert body["requires_deposit"] is False
    assert body["deposit_percentage"] == 0


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
    assert "20%" in combined_text
    assert "desde la web" in combined_text


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
    assert body["requires_deposit"] is True
    assert body["deposit_percentage"] == BOOKING_DEPOSIT_PERCENTAGE
    assert booking_deposit_required_notice() in body["message"]


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
    assert "Cosmetóloga" in combined_text
    assert "estilismo profesional" in combined_text


def test_assistant_chat_rejects_invalid_request():
    response = client.post(
        "/assistant/chat",
        json={
            "session_id": "invalid-session",
            "channel": "web",
        },
    )

    assert response.status_code == 422
