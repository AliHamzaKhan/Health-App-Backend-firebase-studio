from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.v1 import deps
from app.crud import crud_consultation
from app.schemas.consultation import Consultation, ConsultationCreate, ConsultationUpdate
from app.schemas.response import StandardResponse

router = APIRouter()


@router.get("/", response_model=StandardResponse[List[Consultation]])
async def read_consultations(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve consultations.
    """
    consultations = await crud_consultation.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(data=consultations, message="Consultations retrieved successfully.")


@router.post("/", response_model=StandardResponse[Consultation])
async def create_consultation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    consultation_in: ConsultationCreate
):
    """
    Create new consultation.
    """
    consultation = await crud_consultation.create(db, obj_in=consultation_in)
    return StandardResponse(data=consultation, message="Consultation created successfully.")

@router.get("/{id}", response_model=StandardResponse[Consultation])
async def read_consultation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    """
    Get consultation by ID.
    """
    consultation = await crud_consultation.get(db, id=id)
    if not consultation:
        return StandardResponse(success=False, message="Consultation not found", data=None)
    return StandardResponse(data=consultation, message="Consultation retrieved successfully.")

@router.put("/{id}", response_model=StandardResponse[Consultation])
async def update_consultation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    consultation_in: ConsultationUpdate
):
    """
    Update consultation.
    """
    consultation = await crud_consultation.get(db, id=id)
    if not consultation:
        return StandardResponse(success=False, message="Consultation not found", data=None)
    consultation = await crud_consultation.update(db, db_obj=consultation, obj_in=consultation_in)
    return StandardResponse(data=consultation, message="Consultation updated successfully.")

@router.delete("/{id}", response_model=StandardResponse[Consultation])
async def delete_consultation(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    """
    Delete consultation.
    """
    consultation = await crud_consultation.get(db, id=id)
    if not consultation:
        return StandardResponse(success=False, message="Consultation not found", data=None)
    consultation = await crud_consultation.remove(db, id=id)
    return StandardResponse(data=consultation, message="Consultation deleted successfully.")