from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.schemas.response import StandardResponse

router = APIRouter()


@router.get("/", response_model=StandardResponse[List[schemas.Allergy]])
def read_allergies(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve allergies.
    """
    allergies = crud.crud_allergy.get_multi(db=db)
    return StandardResponse(data=allergies)


@router.post("/", response_model=StandardResponse[schemas.Allergy])
def create_allergy(
    *, 
    db: Session = Depends(deps.get_db),
    allergy_in: schemas.AllergyCreate
) -> Any:
    """
    Create new allergy.
    """
    allergy = crud.crud_allergy.create(db=db, obj_in=allergy_in)
    return StandardResponse(data=allergy, message="Allergy created successfully.")


@router.put("/{id}", response_model=StandardResponse[schemas.Allergy])
def update_allergy(
    *, 
    db: Session = Depends(deps.get_db),
    id: int,
    allergy_in: schemas.AllergyUpdate,
) -> Any:
    """
    Update an allergy.
    """
    allergy = crud.crud_allergy.get(db=db, id=id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    allergy = crud.crud_allergy.update(db=db, db_obj=allergy, obj_in=allergy_in)
    return StandardResponse(data=allergy, message="Allergy updated successfully.")


@router.delete("/{id}", response_model=StandardResponse[schemas.Allergy])
def delete_allergy(
    *, 
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Delete an allergy.
    """
    allergy = crud.crud_allergy.get(db=db, id=id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    allergy = crud.crud_allergy.remove(db=db, id=id)
    return StandardResponse(data=allergy, message="Allergy deleted successfully.")
