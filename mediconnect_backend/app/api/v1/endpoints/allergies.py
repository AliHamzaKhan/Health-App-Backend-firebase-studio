from fastapi import APIRouter
from app.schemas.response import StandardResponse
from typing import List, Dict, Any

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[Dict[str, Any]]])
def read_allergies():
    return StandardResponse(data=[{"allergy": "Pollen"}], message="Allergies retrieved successfully.")
