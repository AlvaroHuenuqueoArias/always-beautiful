def test_forgot_password_returns_generic_message(client):
    response = client.post(
        "/auth/forgot-password",
        json={"email": "owner@example.com"},
    )

    assert response.status_code == 200
    body = response.json()

    assert (
        body["message"]
        == "If the account exists, a reset token has been generated."
    )
    assert isinstance(body["reset_token"], str)


def test_forgot_password_for_unknown_email_returns_same_message(client):
    response = client.post(
        "/auth/forgot-password",
        json={"email": "unknown@example.com"},
    )

    assert response.status_code == 200
    body = response.json()

    assert (
        body["message"]
        == "If the account exists, a reset token has been generated."
    )
    assert body["reset_token"] is None


def test_reset_password_fails_with_invalid_token(client):
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-token-1234567890",
            "new_password": "NewOwnerPass123!",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["message"] == "Invalid or expired reset token"


def test_reset_password_allows_login_with_new_password(client):
    forgot_response = client.post(
        "/auth/forgot-password",
        json={"email": "owner@example.com"},
    )
    reset_token = forgot_response.json()["reset_token"]

    reset_response = client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "NewOwnerPass123!",
        },
    )

    assert reset_response.status_code == 200
    assert reset_response.json()["message"] == "Password updated successfully."

    login_response = client.post(
        "/auth/login",
        json={
            "identifier": "owner@example.com",
            "password": "NewOwnerPass123!",
        },
    )

    assert login_response.status_code == 200