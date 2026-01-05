from typing import Dict

from httpx import AsyncClient

from app.core.config import settings


async def test_create_consultation(client: AsyncClient, doctor_auth_headers: Dict[str, str]) -> None:
    response = await client.post(
        f'{settings.API_V1_STR}/consultations/',
        headers=doctor_auth_headers,
        json={
            'appointment_id': 1,
            'notes': 'Test notes'
        }
    )
    assert response.status_code == 200
    content = response.json()
    assert content['notes'] == 'Test notes'
    assert 'id' in content