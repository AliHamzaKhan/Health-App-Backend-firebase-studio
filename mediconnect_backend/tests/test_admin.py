from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_get_doctors_pending_verification(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/admin/doctors/pending-verification")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
