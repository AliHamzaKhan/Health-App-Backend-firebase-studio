from fastapi import APIRouter
from app.schemas.response import StandardResponse
from typing import List, Dict, Any

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[Dict[str, Any]]])
def read_calories():
    return StandardResponse(data=[{"calories": 2000}], message="Calories retrieved successfully.")
