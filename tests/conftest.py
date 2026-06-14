import pytest

from app import app as flask_app
from auth import generate_token


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def valid_token():
    return generate_token("alice")
