from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, List

from app import crud
from app.api import deps
from app.schemas.medication import Medication, MedicationCreate, MedicationUpdate
from app.schemas.response import StandardResponse

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[Medication]])
def read_medications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve medications.
    """
    medications = crud.crud_medication.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(data=medications, message="Medications retrieved successfully.")

@router.post("/", response_model=StandardResponse[Medication])
def create_medicine(
    *,
    db: Session = Depends(deps.get_db),
    medicine_in: MedicationCreate,
) -> Any:
    """
    Create new medicine.
    """
    medicine = crud.crud_medication.create(db, obj_in=medicine_in)
    return StandardResponse(data=medicine, message="Medication created successfully.")

@router.put("/{id}", response_model=StandardResponse[Medication])
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
        return StandardResponse(success=False, message="Medication not found")
    medicine = crud.crud_medication.update(db, db_obj=medicine, obj_in=medicine_in)
    return StandardResponse(data=medicine, message="Medication updated successfully.")

@router.get("/{id}", response_model=StandardResponse[Medication])
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
        return StandardResponse(success=False, message="Medication not found")
    return StandardResponse(data=medicine, message="Medication retrieved successfully.")

@router.delete("/{id}", response_model=StandardResponse[Medication])
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
        return StandardResponse(success=False, message="Medication not found")
    medicine = crud.crud_medication.remove(db, id=id)
    return StandardResponse(data=medicine, message="Medication deleted successfully.")
