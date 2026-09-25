import os

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-signing-key-with-at-least-thirty-two-characters")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "10000")

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def database_schema():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def register_and_login(client: TestClient, email: str) -> dict[str, str]:
    response = client.post(
        "/auth/register",
        json={"email": email, "password": "StrongPassword1!"},
    )
    assert response.status_code == 201
    token = client.post(
        "/auth/login",
        json={"email": email, "password": "StrongPassword1!"},
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}