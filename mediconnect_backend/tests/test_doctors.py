from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.doctor import DoctorCreate


def test_create_doctor(client: TestClient, db: Session) -> None:
    data = {
        "specialization": "Cardiology",
        "yearsOfExperience": 10,
        "bio": "Experienced cardiologist.",
        "languages": ["English", "Spanish"],
        "education": ["MD from Harvard Medical School"],
        "certifications": ["Board Certified in Cardiology"]
    }
    response = client.post(f"{settings.API_V1_STR}/doctors/", json=data)
    assert response.status_code == 200
    created_doctor = response.json()
    assert "id" in created_doctor
    assert created_doctor["specialization"] == data["specialization"]


def test_read_doctors(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/doctors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
