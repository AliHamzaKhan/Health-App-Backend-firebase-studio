from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_calories():
    return [{"calories": 2000}]
