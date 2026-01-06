from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List

from app import crud
from app.api import deps
from app.schemas.medication import Medication, MedicationCreate, MedicationUpdate

router = APIRouter()

@router.get("/", response_model=List[Medication])
def read_medications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve medications.
    """
    medications = crud.crud_medication.get_multi(db, skip=skip, limit=limit)
    return medications

@router.post("/", response_model=Medication)
def create_medicine(
    *,
    db: Session = Depends(deps.get_db),
    medicine_in: MedicationCreate,
) -> Any:
    """
    Create new medicine.
    """
    medicine = crud.crud_medication.create(db, obj_in=medicine_in)
    return medicine

@router.put("/{id}", response_model=Medication)
def update_medicine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    medicine_in: MedicationUpdate,
) -> Any:
    """
    Update a medicine.
    """
    medicine = crud.crud_medication.get(db, id=id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    medicine = crud.crud_medication.update(db, db_obj=medicine, obj_in=medicine_in)
    return medicine

@router.get("/{id}", response_model=Medication)
def read_medicine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get medicine by ID.
    """
    medicine = crud.crud_medication.get(db, id=id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.delete("/{id}", response_model=Medication)
def delete_medicine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a medicine.
    """
    medicine = crud.crud_medication.get(db, id=id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    medicine = crud.crud_medication.remove(db, id=id)
    return medicine
