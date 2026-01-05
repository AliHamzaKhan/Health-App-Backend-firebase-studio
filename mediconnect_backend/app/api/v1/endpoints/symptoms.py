from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_symptoms():
    return [{"symptom": "Headache"}]
