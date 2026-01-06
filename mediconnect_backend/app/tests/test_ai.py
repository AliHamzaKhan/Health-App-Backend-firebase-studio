import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

class TestAI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("google.generativeai.GenerativeModel")
    def test_generate_soap_note(self, mock_gemini):
        mock_gemini.return_value.generate_content.return_value.text = "This is a test SOAP note."

        with open("test_audio.wav", "wb") as f:
            f.write(b"dummy audio data")

        with open("test_audio.wav", "rb") as f:
            response = self.client.post(
                "/api/v1/ai/generate-soap-note",
                files={"audio_file": ("test_audio.wav", f, "audio/wav")},
                data={"context": "Test context"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"generated_text": "This is a test SOAP note."})
        os.remove("test_audio.wav")

    @patch("google.generativeai.GenerativeModel")
    def test_report_analysis(self, mock_gemini):
        mock_gemini.return_value.generate_content.return_value.text = "This is a test summary."
        response = self.client.post("/api/v1/ai/report-analysis", json={"report": "This is a test report."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"summary": "This is a test summary."})

    @patch("google.generativeai.GenerativeModel")
    def test_symptom_checker(self, mock_gemini):
        mock_gemini.return_value.generate_content.return_value.text = '''{"assessment": "Potential cold", "recommended_action": "Rest and drink fluids"}'''
        response = self.client.post("/api/v1/ai/symptom-checker", json={"symptoms": ["cough", "sore throat"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"assessment": "Potential cold", "recommended_action": "Rest and drink fluids"})

    @patch("google.generativeai.GenerativeModel")
    def test_allergy_checker(self, mock_gemini):
        mock_gemini.return_value.generate_content.return_value.text = '''{"is_allergy": true, "confidence": 0.8, "potential_allergens": ["pollen", "dust mites"]}'''
        response = self.client.post("/api/v1/ai/allergy-checker", json={"symptoms": ["runny nose", "sneezing"], "medical_history": ["hay fever"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"is_allergy": True, "confidence": 0.8, "potential_allergens": ["pollen", "dust mites"]})

    @patch("google.generativeai.GenerativeModel")
    def test_calorie_checker(self, mock_gemini):
        mock_gemini.return_value.generate_content.return_value.text = '''{"calories": 200, "breakdown": {"protein": 10, "carbohydrates": 20, "fat": 5}}'''
        response = self.client.post("/api/v1/ai/calorie-checker", json={"meal_description": "two slices of bread"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"calories": 200, "breakdown": {"protein": 10, "carbohydrates": 20, "fat": 5}})

if __name__ == "__main__":
    unittest.main()
