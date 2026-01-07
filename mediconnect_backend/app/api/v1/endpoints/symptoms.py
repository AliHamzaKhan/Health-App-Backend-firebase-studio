from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_symptom import symptom
from app.schemas.symptom import Symptom, SymptomCreate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Symptom])
async def read_symptoms(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve symptoms.
    """
    symptoms = await symptom.get_multi(db, skip=skip, limit=limit)
    return symptoms

@router.post("/", response_model=Symptom)
async def create_symptom(
    symptom_in: SymptomCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create a new symptom.
    """
    symptom_obj = await symptom.create(db, obj_in=symptom_in)
    return symptom_obj
