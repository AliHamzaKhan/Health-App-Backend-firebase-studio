from pydantic import BaseModel
from typing import List

class ReportAnalysisRequest(BaseModel):
    report: str

class ReportAnalysisResponse(BaseModel):
    summary: str

class SymptomCheckerRequest(BaseModel):
    symptoms: List[str]

class SymptomCheckerResponse(BaseModel):
    assessment: str
    recommended_action: str

class AllergyCheckerRequest(BaseModel):
    symptoms: List[str]
    medical_history: List[str]

class AllergyCheckerResponse(BaseModel):
    is_allergy: bool
    confidence: float
    potential_allergens: List[str]

class CalorieCheckerRequest(BaseModel):
    meal_description: str

class CalorieCheckerResponse(BaseModel):
    calories: int
    breakdown: dict
