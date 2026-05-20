def test_create_booking_deposit_draft_with_tentative_schedule(client):
    payload = {
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
    assert body["status"] == "draft"
    assert body["source"] == "assistant"
    assert body["deposit_percentage"] == 20
    assert body["remaining_percentage"] == 80
    assert body["total_amount"] == 50000
    assert body["deposit_amount"] == 10000
    assert body["remaining_amount"] == 40000
    assert body["amount_status"] == "estimated"
    assert body["schedule_status"] == "pending_confirmation"
    assert body["confirmation_status"] == "not_confirmed"
    assert body["payment_status"] == "not_executed"
    assert body["booking_status"] == "not_created"
    assert body["order_status"] == "not_created"
    assert body["requested_day"] == "miercoles"
    assert body["requested_time"] == "15:00"
    assert body["cart_count"] == 1
    assert len(body["items"]) == 1

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


def test_create_booking_deposit_draft_without_price_keeps_pending_amount(client):
    response = client.post(
        "/cart/booking-deposit/draft",
        json={
            "service_label": "Brushing",
            "professional_label": "Maria Ignacia",
            "professional_id": "maria_ignacia",
            "professional_role": "Cosmetologa",
            "source": "assistant",
        },
    )

    assert response.status_code == 201
    body = response.json()

    assert body["status"] == "draft"
    assert body["total_amount"] is None
    assert body["deposit_amount"] is None
    assert body["remaining_amount"] is None
    assert body["amount_status"] == "pending_final_price"
    assert body["schedule_status"] == "pending_selection"
    assert body["confirmation_status"] == "not_confirmed"
    assert body["payment_status"] == "not_executed"
    assert body["booking_status"] == "not_created"
    assert body["order_status"] == "not_created"
    assert body["cart_count"] == 1
    assert body["items"][0]["amount_status"] == "pending_final_price"
    assert body["items"][0]["deposit_amount"] is None
    assert body["items"][0]["remaining_amount"] is None


def test_booking_deposit_draft_id_is_deterministic(client):
    payload = {
        "service_label": "Peinado social",
        "professional_label": "Nadia Luisa",
        "professional_id": "nadia_luisa",
        "professional_role": "Estilista profesional",
        "requested_day": "sabado",
        "requested_time": "10:30",
        "service_price": 30000,
        "source": "assistant",
    }

    first_response = client.post("/cart/booking-deposit/draft", json=payload)
    second_response = client.post("/cart/booking-deposit/draft", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["draft_id"] == second_response.json()["draft_id"]


def test_booking_deposit_draft_rejects_missing_required_data(client):
    response = client.post(
        "/cart/booking-deposit/draft",
        json={
            "service_label": "Limpieza facial",
        },
    )

    assert response.status_code == 422
