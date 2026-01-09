from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.schemas.calorie import CalorieCreate, CalorieUpdate

settings = get_settings()

def test_create_calorie(client: TestClient, db: Session) -> None:
    data = {"name": "Apple", "calories": 95}
    response = client.post(
        f"{settings.API_V1_STR}/calories/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert content["data"]["name"] == data["name"]
    assert "id" in content["data"]

def test_read_calories(client: TestClient, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/calories/")
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert isinstance(content["data"], list)
    assert len(content["data"]) > 0

def test_update_calorie(client: TestClient, db: Session) -> None:
    # First, create a calorie to update
    create_data = {"name": "Banana", "calories": 105}
    create_response = client.post(f"{settings.API_V1_STR}/calories/", json=create_data)
    calorie_id = create_response.json()["data"]["id"]

    # Now, update it
    update_data = {"name": "Big Banana", "calories": 150}
    response = client.put(
        f"{settings.API_V1_STR}/calories/{calorie_id}",
        json=update_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert content["data"]["name"] == update_data["name"]
    assert content["data"]["calories"] == update_data["calories"]
    assert content["data"]["id"] == calorie_id

def test_delete_calorie(client: TestClient, db: Session) -> None:
    # First, create a calorie to delete
    create_data = {"name": "Orange", "calories": 45}
    create_response = client.post(f"{settings.API_V1_STR}/calories/", json=create_data)
    calorie_id = create_response.json()["data"]["id"]

    # Now, delete it
    response = client.delete(f"{settings.API_V1_STR}/calories/{calorie_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["success"] == True
    assert content["data"]["id"] == calorie_id

    # Verify it's deleted
    get_response = client.get(f"{settings.API_V1_STR}/calories/{calorie_id}")
    assert get_response.status_code == 404
