import json


class TestRegister:
    def test_register_success(self, client):
        resp = client.post(
            "/api/auth/register",
            json={
                "phone": "1234567890",
                "email": "new@example.com",
                "password": "password123",
                "firstname": "New",
                "lastname": "User",
            },
        )
        assert resp.status_code == 201

    def test_register_missing_fields(self, client):
        resp = client.post(
            "/api/auth/register",
            json={"email": "inc@example.com"},
        )
        assert resp.status_code == 400

    def test_register_duplicate_email(self, client):
        data = {
            "phone": "1234567890",
            "email": "dup@example.com",
            "password": "password123",
            "firstname": "Dup",
            "lastname": "User",
        }
        client.post("/api/auth/register", json=data)
        resp = client.post("/api/auth/register", json=data)
        assert resp.status_code == 400


class TestLogin:
    def test_login_success(self, client):
        client.post(
            "/api/auth/register",
            json={
                "phone": "1234567890",
                "email": "login@example.com",
                "password": "password123",
                "firstname": "Login",
                "lastname": "User",
            },
        )
        resp = client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "password123"},
        )
        assert resp.status_code == 200
        assert "access_token" in resp.get_json()

    def test_login_wrong_password(self, client):
        client.post(
            "/api/auth/register",
            json={
                "phone": "1234567890",
                "email": "wrong@example.com",
                "password": "password123",
                "firstname": "Wrong",
                "lastname": "User",
            },
        )
        resp = client.post(
            "/api/auth/login",
            json={"email": "wrong@example.com", "password": "wrongpass"},
        )
        assert resp.status_code in (400, 401)

    def test_login_nonexistent_user(self, client):
        resp = client.post(
            "/api/auth/login",
            json={"email": "ghost@example.com", "password": "pass"},
        )
        assert resp.status_code in (400, 401)


class TestGetCurrentUser:
    def test_get_me_authenticated(self, client, auth_headers):
        resp = client.get("/api/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"

    def test_get_me_unauthenticated(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code in (401, 422)
