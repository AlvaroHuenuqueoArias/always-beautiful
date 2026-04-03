from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _login_as_owner() -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={
            "identifier": "owner@example.com",
            "password": "OwnerPass123!",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _login_as_technical() -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={
            "identifier": "tech@example.com",
            "password": "TechPass123!",
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_system_health_returns_ok():
    response = client.get("/system/health")

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "ok"
    assert "timestamp" in body


def test_system_info_requires_authentication():
    response = client.get("/system/info")

    assert response.status_code == 401


def test_system_info_returns_service_metadata_for_authenticated_admin():
    headers = _login_as_owner()
    response = client.get("/system/info", headers=headers)

    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "always-beautiful-api"
    assert body["version"] == "0.1.0"
    assert body["environment"] == "test"


def test_system_metrics_returns_real_counters_for_technical_admin():
    headers = _login_as_technical()

    client.get("/system/health")
    client.get("/system/info", headers=headers)

    response = client.get("/system/metrics", headers=headers)

    assert response.status_code == 200
    body = response.json()

    assert "started_at" in body
    assert isinstance(body["uptime_seconds"], int)
    assert isinstance(body["requests_total"], int)
    assert isinstance(body["http_errors_total"], int)
    assert isinstance(body["unhandled_errors_total"], int)
    assert body["requests_total"] >= 4


def test_system_metrics_rejects_owner_role():
    headers = _login_as_owner()
    response = client.get("/system/metrics", headers=headers)

    assert response.status_code == 403
    assert (
        response.json()["error"]["message"]
        == "Technical administrator permissions are required"
    )


def test_security_headers_are_applied():
    response = client.get("/system/health")

    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"