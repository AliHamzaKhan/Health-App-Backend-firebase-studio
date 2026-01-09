import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers

class TestMedications(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.superuser_token_headers = get_superuser_token_headers(self.client)

    def test_get_medications(self):
        response = self.client.get(f"{settings.API_V1_STR}/medications/", headers=self.superuser_token_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

    def test_create_medication(self):
        medication_data = {"name": "Test Medication", "dosage": "10mg", "frequency": "Once a day"}
        response = self.client.post(f"{settings.API_V1_STR}/medications/", json=medication_data, headers=self.superuser_token_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["name"], "Test Medication")

if __name__ == "__main__":
    unittest.main()
