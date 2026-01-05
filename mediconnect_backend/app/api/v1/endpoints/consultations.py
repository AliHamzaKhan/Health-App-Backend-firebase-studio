from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.v1 import deps
from app.crud import crud_consultation
from app.schemas.consultation import Consultation, ConsultationCreate, ConsultationUpdate

router = APIRouter()


@router.get("/", response_model=List[Consultation])
async def read_consultations(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve consultations.
    """
    consultations = await crud_consultation.get_multi(db, skip=skip, limit=limit)
    return consultations


@router.post("/", response_model=Consultation)
async def create_consultation(
    *, 
    db: AsyncSession = Depends(deps.get_db), 
    consultation_in: ConsultationCreate
):
    """
    Create new consultation.
    """
    consultation = await crud_consultation.create(db, obj_in=consultation_in)
    return consultation

@router.get("/{id}", response_model=Consultation)
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
        raise HTTPException(status_code=404, detail="Consultation not found")
    return consultation

@router.put("/{id}", response_model=Consultation)
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
        raise HTTPException(status_code=404, detail="Consultation not found")
    consultation = await crud_consultation.update(db, db_obj=consultation, obj_in=consultation_in)
    return consultation

@router.delete("/{id}", response_model=Consultation)
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
        raise HTTPException(status_code=404, detail="Consultation not found")
    consultation = await crud_consultation.remove(db, id=id)
    return consultation
