def _login(client, identifier: str, password: str) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"identifier": identifier, "password": password},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_dashboard_requires_authentication(client):
    response = client.get("/admin/dashboard")
    assert response.status_code == 401


def test_admin_dashboard_allows_authenticated_admin(client):
    headers = _login(client, "owner@example.com", "OwnerPass123!")
    response = client.get("/admin/dashboard", headers=headers)

    assert response.status_code == 200
    body = response.json()

    assert "kpis" in body
    assert "recent_orders" in body


def test_system_info_requires_authentication(client):
    response = client.get("/system/info")
    assert response.status_code == 401


def test_system_info_allows_authenticated_admin(client):
    headers = _login(client, "owner@example.com", "OwnerPass123!")
    response = client.get("/system/info", headers=headers)

    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "always-beautiful-api"
    assert body["version"] == "0.1.0"


def test_system_metrics_requires_technical_admin_role(client):
    owner_headers = _login(client, "owner@example.com", "OwnerPass123!")
    response = client.get("/system/metrics", headers=owner_headers)

    assert response.status_code == 403
    assert (
        response.json()["error"]["message"]
        == "Technical administrator permissions are required"
    )


def test_system_metrics_allows_technical_admin(client):
    technical_headers = _login(client, "tech@example.com", "TechPass123!")
    response = client.get("/system/metrics", headers=technical_headers)

    assert response.status_code == 200
    body = response.json()

    assert "requests_total" in body
    assert "http_errors_total" in body