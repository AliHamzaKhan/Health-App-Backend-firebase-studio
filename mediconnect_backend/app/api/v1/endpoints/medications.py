from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List

from app import crud
from app.api import deps
from app.schemas.medicine import Medicine, MedicineCreate, MedicineUpdate

router = APIRouter()

@router.get("/", response_model=List[Medicine])
def read_medications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve medications.
    """
    medications = crud.crud_medicine.get_multi(db, skip=skip, limit=limit)
    return medications

@router.post("/", response_model=Medicine)
def create_medicine(
    *,
    db: Session = Depends(deps.get_db),
    medicine_in: MedicineCreate,
) -> Any:
    """
    Create new medicine.
    """
    medicine = crud.crud_medicine.create(db, obj_in=medicine_in)
    return medicine

@router.put("/{id}", response_model=Medicine)
def update_medicine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    medicine_in: MedicineUpdate,
) -> Any:
    """
    Update a medicine.
    """
    medicine = crud.crud_medicine.get(db, id=id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    medicine = crud.crud_medicine.update(db, db_obj=medicine, obj_in=medicine_in)
    return medicine

@router.get("/{id}", response_model=Medicine)
def read_medicine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get medicine by ID.
    """
    medicine = crud.crud_medicine.get(db, id=id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.delete("/{id}", response_model=Medicine)
def delete_medicine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a medicine.
    """
    medicine = crud.crud_medicine.get(db, id=id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    medicine = crud.crud_medicine.remove(db, id=id)
    return medicine
