from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_system_health_returns_ok():
    response = client.get("/system/health")

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "ok"
    assert "timestamp" in body


def test_system_info_returns_service_metadata():
    response = client.get("/system/info")

    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "always-beautiful-api"
    assert body["version"] == "0.1.0"
    assert body["environment"] == "development"


def test_system_metrics_returns_real_counters():
    client.get("/system/health")
    client.get("/system/info")

    response = client.get("/system/metrics")

    assert response.status_code == 200
    body = response.json()

    assert "started_at" in body
    assert isinstance(body["uptime_seconds"], int)
    assert isinstance(body["requests_total"], int)
    assert isinstance(body["http_errors_total"], int)
    assert isinstance(body["unhandled_errors_total"], int)
    assert body["requests_total"] >= 3


def test_security_headers_are_applied():
    response = client.get("/system/health")

    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"