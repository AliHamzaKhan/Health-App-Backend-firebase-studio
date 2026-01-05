from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_create_consultation(client: TestClient, db: Session) -> None:
    data = {
        "appointment_id": 1,
        "hpi": "Patient reports intermittent chest pain.",
        "soap_note": "S: Chest pain. O: BP 130/85. A: Angina. P: Nitroglycerin.",
        "icd_codes": "I20.9",
        "treatment_plan": "Lifestyle modifications.",
        "prescribed_medicines": [
            {
                "name": "Nitroglycerin",
                "dosage": "0.4mg",
                "frequency": "As needed"
            }
        ],
        "recommended_lab_tests": ["Lipid Panel"]
    }
    response = client.post(f"{settings.API_V1_STR}/consultations/", json=data)
    assert response.status_code == 200
    created_consultation = response.json()
    assert "id" in created_consultation
    assert created_consultation["hpi"] == data["hpi"]


def test_read_consultations(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/consultations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
