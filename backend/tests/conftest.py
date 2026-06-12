import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["MAIL_SERVER"] = "localhost"
os.environ["MAIL_PORT"] = "25"

from app import create_app
from api.models import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    return app


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Register a user and return auth headers."""
    client.post(
        "/api/auth/register",
        json={
            "phone": "1234567890",
            "email": "test@example.com",
            "password": "password123",
            "firstname": "Test",
            "lastname": "User",
            "address": "123 Test St",
        },
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, db):
    """Create an admin user and return auth headers."""
    from api.models import User, UserRole

    with client.application.app_context():
        admin = User(
            email="admin@test.com",
            role=UserRole.admin,
            phone="9999999999",
            firstname="Admin",
            lastname="User",
            address="Admin Office",
        )
        admin.set_password("admin123")
        _db.session.add(admin)
        _db.session.commit()
        admin_id = admin.id

    resp = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
