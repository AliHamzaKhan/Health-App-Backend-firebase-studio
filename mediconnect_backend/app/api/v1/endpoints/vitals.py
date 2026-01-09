from fastapi import APIRouter, Depends
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_vital import vital
from app.schemas.vital import Vital, VitalCreate, VitalUpdate
from app.models.user import User
from app.schemas.response import StandardResponse

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[Vital]])
async def read_vitals(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve vitals.
    """
    vitals = await vital.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(data=vitals, message="Vitals retrieved successfully.")

@router.post("/", response_model=StandardResponse[Vital])
async def create_vital(
    vital_in: VitalCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create a new vital.
    """
    vital_obj = await vital.create(db, obj_in=vital_in)
    return StandardResponse(data=vital_obj, message="Vital created successfully.")

@router.get("/{vital_id}", response_model=StandardResponse[Vital])
async def read_vital(
    vital_id: int,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get vital by ID.
    """
    vital_obj = await vital.get(db, id=vital_id)
    if not vital_obj:
        return StandardResponse(success=False, message="Vital not found")
    return StandardResponse(data=vital_obj, message="Vital retrieved successfully.")

@router.put("/{vital_id}", response_model=StandardResponse[Vital])
async def update_vital(
    vital_id: int,
    vital_in: VitalUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update a vital.
    """
    vital_obj = await vital.get(db, id=vital_id)
    if not vital_obj:
        return StandardResponse(success=False, message="Vital not found")
    vital_obj = await vital.update(db, db_obj=vital_obj, obj_in=vital_in)
    return StandardResponse(data=vital_obj, message="Vital updated successfully.")

@router.delete("/{vital_id}", response_model=StandardResponse[Vital])
async def delete_vital(
    vital_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a vital.
    """
    vital_obj = await vital.get(db, id=vital_id)
    if not vital_obj:
        return StandardResponse(success=False, message="Vital not found")
    vital_obj = await vital.remove(db, id=vital_id)
    return StandardResponse(data=vital_obj, message="Vital deleted successfully.")
