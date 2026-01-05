from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_vitals():
    return [{"vital_name": "Heart Rate", "value": "70 bpm"}]
