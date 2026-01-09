from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.schemas.response import StandardResponse

router = APIRouter()


@router.get("/", response_model=StandardResponse[List[schemas.Calorie]])
def read_calories(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve calories.
    """
    calories = crud.crud_calorie.crud_calorie.get_multi(db=db)
    return StandardResponse(data=calories)


@router.post("/", response_model=StandardResponse[schemas.Calorie])
def create_calorie(
    *,
    db: Session = Depends(deps.get_db),
    calorie_in: schemas.CalorieCreate
) -> Any:
    """
    Create new calorie.
    """
    calorie = crud.crud_calorie.create(db=db, obj_in=calorie_in)
    return StandardResponse(data=calorie, message="Calorie created successfully.")


@router.put("/{id}", response_model=StandardResponse[schemas.Calorie])
def update_calorie(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    calorie_in: schemas.CalorieUpdate,
) -> Any:
    """
    Update a calorie.
    """
    calorie = crud.crud_calorie.get(db=db, id=id)
    if not calorie:
        raise HTTPException(status_code=404, detail="Calorie not found")
    calorie = crud.crud_calorie.update(db=db, db_obj=calorie, obj_in=calorie_in)
    return StandardResponse(data=calorie, message="Calorie updated successfully.")


@router.delete("/{id}", response_model=StandardResponse[schemas.Calorie])
def delete_calorie(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Delete a calorie.
    """
    calorie = crud.crud_calorie.get(db=db, id=id)
    if not calorie:
        raise HTTPException(status_code=404, detail="Calorie not found")
    calorie = crud.crud_calorie.remove(db=db, id=id)
    return StandardResponse(data=calorie, message="Calorie deleted successfully.")
