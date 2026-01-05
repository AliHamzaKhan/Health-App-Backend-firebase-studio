from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_allergies():
    return [{"allergy": "Pollen"}]
