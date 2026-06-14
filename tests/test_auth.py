import json


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_login_success(client):
    response = client.post(
        "/login",
        data=json.dumps({"username": "alice", "password": "pass123"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data


def test_login_wrong_password(client):
    response = client.post(
        "/login",
        data=json.dumps({"username": "alice", "password": "wrongpass"}),
        content_type="application/json",
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"


def test_login_wrong_username(client):
    response = client.post(
        "/login",
        data=json.dumps({"username": "nobody", "password": "pass123"}),
        content_type="application/json",
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"


def test_login_missing_username(client):
    response = client.post(
        "/login",
        data=json.dumps({"password": "pass123"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_token_is_valid_jwt_format(client):
    response = client.post(
        "/login",
        data=json.dumps({"username": "alice", "password": "pass123"}),
        content_type="application/json",
    )
    token = response.get_json()["token"]
    parts = token.split(".")
    assert len(parts) == 3
