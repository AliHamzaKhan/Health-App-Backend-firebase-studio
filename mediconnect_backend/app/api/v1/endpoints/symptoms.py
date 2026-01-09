from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_symptom import symptom
from app.schemas.symptom import Symptom, SymptomCreate, SymptomUpdate
from app.models.user import User
from app.schemas.response import StandardResponse

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[Symptom]])
async def read_symptoms(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve symptoms.
    """
    symptoms = await symptom.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(data=symptoms, message="Symptoms retrieved successfully.")

@router.post("/", response_model=StandardResponse[Symptom])
async def create_symptom(
    symptom_in: SymptomCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create a new symptom.
    """
    symptom_obj = await symptom.create(db, obj_in=symptom_in)
    return StandardResponse(data=symptom_obj, message="Symptom created successfully.")

@router.get("/{symptom_id}", response_model=StandardResponse[Symptom])
async def read_symptom(
    symptom_id: int,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get symptom by ID.
    """
    symptom_obj = await symptom.get(db, id=symptom_id)
    if not symptom_obj:
        return StandardResponse(success=False, message="Symptom not found")
    return StandardResponse(data=symptom_obj, message="Symptom retrieved successfully.")

@router.put("/{symptom_id}", response_model=StandardResponse[Symptom])
async def update_symptom(
    symptom_id: int,
    symptom_in: SymptomUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update a symptom.
    """
    symptom_obj = await symptom.get(db, id=symptom_id)
    if not symptom_obj:
        return StandardResponse(success=False, message="Symptom not found")
    symptom_obj = await symptom.update(db, db_obj=symptom_obj, obj_in=symptom_in)
    return StandardResponse(data=symptom_obj, message="Symptom updated successfully.")

@router.delete("/{symptom_id}", response_model=StandardResponse[Symptom])
async def delete_symptom(
    symptom_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a symptom.
    """
    symptom_obj = await symptom.get(db, id=symptom_id)
    if not symptom_obj:
        return StandardResponse(success=False, message="Symptom not found")
    symptom_obj = await symptom.remove(db, id=symptom_id)
    return StandardResponse(data=symptom_obj, message="Symptom deleted successfully.")
