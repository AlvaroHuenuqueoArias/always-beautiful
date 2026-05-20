def assert_draft_non_final_states(body):
    assert body["status"] == "draft"
    assert body["confirmation_status"] == "not_confirmed"
    assert body["payment_status"] == "not_executed"
    assert body["booking_status"] == "not_created"
    assert body["order_status"] == "not_created"


def build_multi_service_payload(assistant_session_id="assistant-session-1"):
    return {
        "assistant_session_id": assistant_session_id,
        "source": "assistant",
        "requested_day": "miercoles",
        "requested_time": "15:00",
        "items": [
            {
                "service_label": "Limpieza facial",
                "professional_label": "Maria Ignacia",
                "professional_id": "maria_ignacia",
                "professional_role": "Cosmetologa",
                "service_price": 50000,
            },
            {
                "service_label": "Brushing",
                "professional_label": "Maria Ignacia",
                "professional_id": "maria_ignacia",
                "professional_role": "Cosmetologa",
                "service_price": 30000,
            },
        ],
    }


def test_create_booking_deposit_draft_with_single_service_item(client):
    payload = {
        "assistant_session_id": "assistant-single-service",
        "service_label": "Limpieza facial",
        "professional_label": "Maria Ignacia",
        "professional_id": "maria_ignacia",
        "professional_role": "Cosmetologa",
        "requested_day": "miercoles",
        "requested_time": "15:00",
        "service_price": 50000,
        "source": "assistant",
    }

    response = client.post("/cart/booking-deposit/draft", json=payload)

    assert response.status_code == 201
    body = response.json()

    assert body["type"] == "booking_deposit_draft"
    assert body["source"] == "assistant"
    assert body["assistant_session_id"] == "assistant-single-service"
    assert body["deposit_percentage"] == 20
    assert body["remaining_percentage"] == 80
    assert body["total_amount"] == 50000
    assert body["deposit_amount"] == 10000
    assert body["remaining_amount"] == 40000
    assert body["amount_status"] == "estimated"
    assert body["schedule_status"] == "pending_confirmation"
    assert body["requested_day"] == "miercoles"
    assert body["requested_time"] == "15:00"
    assert body["cart_count"] == 1
    assert len(body["items"]) == 1
    assert_draft_non_final_states(body)

    item = body["items"][0]
    assert item["service_label"] == "Limpieza facial"
    assert item["professional_label"] == "Maria Ignacia"
    assert item["professional_id"] == "maria_ignacia"
    assert item["professional_role"] == "Cosmetologa"
    assert item["quantity"] == 1
    assert item["service_price"] == 50000
    assert item["deposit_amount"] == 10000
    assert item["remaining_amount"] == 40000
    assert item["amount_status"] == "estimated"


def test_create_booking_deposit_draft_with_multiple_service_items(client):
    response = client.post(
        "/cart/booking-deposit/draft",
        json=build_multi_service_payload(),
    )

    assert response.status_code == 201
    body = response.json()

    assert body["type"] == "booking_deposit_draft"
    assert body["assistant_session_id"] == "assistant-session-1"
    assert body["total_amount"] == 80000
    assert body["deposit_amount"] == 16000
    assert body["remaining_amount"] == 64000
    assert body["amount_status"] == "estimated"
    assert body["cart_count"] == 2
    assert len(body["items"]) == 2
    assert [item["service_label"] for item in body["items"]] == [
        "Limpieza facial",
        "Brushing",
    ]
    assert [item["deposit_amount"] for item in body["items"]] == [
        10000,
        6000,
    ]
    assert_draft_non_final_states(body)


def test_booking_deposit_draft_without_price_keeps_pending_amount(client):
    response = client.post(
        "/cart/booking-deposit/draft",
        json={
            "assistant_session_id": "assistant-pending-price",
            "source": "assistant",
            "items": [
                {
                    "service_label": "Brushing",
                    "professional_label": "Maria Ignacia",
                    "professional_id": "maria_ignacia",
                    "professional_role": "Cosmetologa",
                }
            ],
        },
    )

    assert response.status_code == 201
    body = response.json()

    assert body["total_amount"] is None
    assert body["deposit_amount"] is None
    assert body["remaining_amount"] is None
    assert body["amount_status"] == "pending_final_price"
    assert body["schedule_status"] == "pending_selection"
    assert body["cart_count"] == 1
    assert body["items"][0]["amount_status"] == "pending_final_price"
    assert body["items"][0]["deposit_amount"] is None
    assert body["items"][0]["remaining_amount"] is None
    assert_draft_non_final_states(body)


def test_booking_deposit_draft_id_uses_assistant_session_id(client):
    payload = build_multi_service_payload("assistant-session-a")

    first_response = client.post("/cart/booking-deposit/draft", json=payload)
    second_response = client.post("/cart/booking-deposit/draft", json=payload)
    different_session_response = client.post(
        "/cart/booking-deposit/draft",
        json=build_multi_service_payload("assistant-session-b"),
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert different_session_response.status_code == 201
    assert first_response.json()["draft_id"] == second_response.json()["draft_id"]
    assert first_response.json()["draft_id"] != (
        different_session_response.json()["draft_id"]
    )


def test_booking_deposit_draft_rejects_invalid_source(client):
    response = client.post(
        "/cart/booking-deposit/draft",
        json={
            **build_multi_service_payload(),
            "source": "invalid_source",
        },
    )

    assert response.status_code == 422


def test_booking_deposit_draft_rejects_invalid_payload(client):
    response = client.post(
        "/cart/booking-deposit/draft",
        json={
            "assistant_session_id": "assistant-invalid-payload",
            "source": "assistant",
            "items": [],
        },
    )

    assert response.status_code == 422
