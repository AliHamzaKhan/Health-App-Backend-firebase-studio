from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_login_access_token(client: TestClient, db: Session) -> None:
    login_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"
