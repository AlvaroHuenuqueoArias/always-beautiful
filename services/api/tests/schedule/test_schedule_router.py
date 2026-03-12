from datetime import date
from fastapi.testclient import TestClient

from app.main import app
from app.schedule.routes import schedule_repository

client = TestClient(app)


def setup_function():
    schedule_repository.reset()


def test_schedule_health():
    response = client.get("/schedule/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_get_empty_template():
    response = client.get("/schedule/template")

    assert response.status_code == 200
    assert response.json() == {
        "weekly_rules": [],
        "breaks": [],
    }


def test_replace_template_success():
    payload = {
        "weekly_rules": [
            {
                "day_of_week": 0,
                "is_working_day": True,
                "start_time": "11:00:00",
                "end_time": "19:00:00",
            }
        ],
        "breaks": [
            {
                "day_of_week": 0,
                "start_time": "14:00:00",
                "end_time": "15:00:00",
                "label": "Lunch",
            }
        ],
    }

    response = client.put("/schedule/template", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert len(body["weekly_rules"]) == 1
    assert len(body["breaks"]) == 1


def test_create_date_block_success():
    template_payload = {
        "weekly_rules": [
            {
                "day_of_week": 0,
                "is_working_day": True,
                "start_time": "11:00:00",
                "end_time": "19:00:00",
            }
        ],
        "breaks": [],
    }

    client.put("/schedule/template", json=template_payload)

    block_payload = {
        "block_date": "2026-03-16",
        "start_time": "16:00:00",
        "end_time": "17:00:00",
        "reason": "Private event",
    }

    response = client.post("/schedule/blocks", json=block_payload)

    assert response.status_code == 201
    assert response.json()["reason"] == "Private event"


def test_create_date_block_rejects_invalid_window():
    template_payload = {
        "weekly_rules": [
            {
                "day_of_week": 0,
                "is_working_day": True,
                "start_time": "11:00:00",
                "end_time": "19:00:00",
            }
        ],
        "breaks": [],
    }

    client.put("/schedule/template", json=template_payload)

    block_payload = {
        "block_date": "2026-03-16",
        "start_time": "10:00:00",
        "end_time": "12:00:00",
        "reason": "Invalid block",
    }

    response = client.post("/schedule/blocks", json=block_payload)

    assert response.status_code == 400


def test_get_day_schedule():
    template_payload = {
        "weekly_rules": [
            {
                "day_of_week": 0,
                "is_working_day": True,
                "start_time": "11:00:00",
                "end_time": "19:00:00",
            }
        ],
        "breaks": [
            {
                "day_of_week": 0,
                "start_time": "14:00:00",
                "end_time": "15:00:00",
                "label": "Lunch",
            }
        ],
    }

    client.put("/schedule/template", json=template_payload)

    response = client.get("/schedule/day/2026-03-16")

    assert response.status_code == 200
    body = response.json()
    assert body["is_working_day"] is True
    assert body["start_time"] == "11:00:00"
    assert body["end_time"] == "19:00:00"
    assert len(body["breaks"]) == 1