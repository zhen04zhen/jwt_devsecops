def test_access_with_valid_token(client, valid_token):
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "authorized"
    assert "alice" in data["message"]


def test_access_without_token(client):
    response = client.get("/protected")
    assert response.status_code == 200
    assert response.get_json()["error"] == "Token missing"


def test_access_with_fake_token(client):
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer fake.token.here"},
    )
    assert response.status_code == 403
    assert response.get_json()["error"] == "Invalid token"


def test_access_with_wrong_header_format(client, valid_token):
    response = client.get(
        "/protected",
        headers={"Authorization": f"Token {valid_token}"},
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"
