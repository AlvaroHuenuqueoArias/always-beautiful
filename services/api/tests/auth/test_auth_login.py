def test_login_returns_access_token_for_owner(client):
    response = client.post(
        "/auth/login",
        json={
            "identifier": "owner-admin",
            "password": "OwnerPass123!",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 1800
    assert body["user"]["username"] == "owner-admin"
    assert body["user"]["role"] == "admin_owner"


def test_login_rejects_invalid_password(client):
    response = client.post(
        "/auth/login",
        json={
            "identifier": "owner-admin",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    body = response.json()

    assert body["error"]["type"] == "http_error"
    assert body["error"]["status_code"] == 401


def test_login_is_rate_limited_after_repeated_failures(client):
    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={
                "identifier": "owner@example.com",
                "password": "WrongPassword123!",
            },
        )
        assert response.status_code == 401

    blocked_response = client.post(
        "/auth/login",
        json={
            "identifier": "owner@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert blocked_response.status_code == 429
    assert (
        blocked_response.json()["error"]["message"]
        == "Too many failed login attempts. Please try again later."
    )