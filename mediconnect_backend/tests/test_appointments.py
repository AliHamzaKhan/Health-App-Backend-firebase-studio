import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings

def test_create_appointment(client: TestClient, db: Session) -> None:
    data = {
        "doctor_id": 1,
        "patient_id": 1,
        "appointment_time": "2025-01-01T12:00:00",
        "status": "scheduled"
    }
    response = client.post(f"{settings.API_V1_STR}/appointments/", json=data)
    assert response.status_code == 200
    created_appointment = response.json()
    assert "id" in created_appointment
    assert created_appointment["status"] == "scheduled"


def test_read_appointments(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/appointments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
