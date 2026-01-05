from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.user import UserCreate


def test_create_user(client: TestClient, db: Session) -> None:
    data = {"email": "test@example.com", "password": "testpassword"}
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=data,
    )
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["email"] == data["email"]
    assert "id" in created_user


def test_read_users(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
