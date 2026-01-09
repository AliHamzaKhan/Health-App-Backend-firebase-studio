from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.schemas.allergy import AllergyCreate, AllergyUpdate

settings = get_settings()

def test_create_allergy(client: TestClient, db: Session) -> None:
    data = {"name": "Pollen"}
    response = client.post(
        f"{settings.API_V1_STR}/allergies/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert content["data"]["name"] == data["name"]
    assert "id" in content["data"]

def test_read_allergies(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/allergies/")
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert isinstance(content["data"], list)
    assert len(content["data"]) > 0

def test_update_allergy(client: TestClient, db: Session) -> None:
    # First, create an allergy to update
    create_data = {"name": "Dust"}
    create_response = client.post(f"{settings.API_V1_STR}/allergies/", json=create_data)
    allergy_id = create_response.json()["data"]["id"]

    # Now, update it
    update_data = {"name": "Dust Mites"}
    response = client.put(
        f"{settings.API_V1_STR}/allergies/{allergy_id}",
        json=update_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert content["data"]["name"] == update_data["name"]
    assert content["data"]["id"] == allergy_id

def test_delete_allergy(client: TestClient, db: Session) -> None:
    # First, create an allergy to delete
    create_data = {"name": "Peanuts"}
    create_response = client.post(f"{settings.API_V1_STR}/allergies/", json=create_data)
    allergy_id = create_response.json()["data"]["id"]

    # Now, delete it
    response = client.delete(f"{settings.API_V1_STR}/allergies/{allergy_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert content["data"]["id"] == allergy_id

    # Verify it's deleted
    get_response = client.get(f"{settings.API_V1_STR}/allergies/{allergy_id}")
    assert get_response.status_code == 404
