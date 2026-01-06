import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.tests.utils.utils import get_superuser_token_headers
from app.db.session import SessionLocal
from app.crud import permission

class TestPermissions(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = SessionLocal()
        self.superuser_token_headers = get_superuser_token_headers(self.client)

    def tearDown(self):
        self.db.close()

    def test_seed_permissions(self):
        response = self.client.post(f"{settings.API_V1_STR}/admin/permissions/seed_permissions/", headers=self.superuser_token_headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Permissions seeded successfully"})

        doctor_permissions = permission.get_by_role(self.db, role="doctor")
        self.assertTrue(doctor_permissions)
        self.assertTrue(doctor_permissions.permissions["viewSchedule"])

        patient_permissions = permission.get_by_role(self.db, role="patient")
        self.assertTrue(patient_permissions)
        self.assertTrue(patient_permissions.permissions["addMedication"])

if __name__ == "__main__":
    unittest.main()
