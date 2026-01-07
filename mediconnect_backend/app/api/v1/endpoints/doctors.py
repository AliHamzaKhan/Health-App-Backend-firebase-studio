from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Doctor])
async def read_doctors(
        db: AsyncSession = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve doctors.
    """
    doctors = await crud.doctor.get_multi(db, skip=skip, limit=limit)
    return doctors


@router.post("/", response_model=schemas.Doctor)
async def create_doctor(
        *,
        db: AsyncSession = Depends(deps.get_db),
        doctor_in: schemas.DoctorCreate,
        current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new doctor.
    """
    doctor = await crud.doctor.get_by_email(db, email=doctor_in.email)
    if doctor:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    doctor = await crud.doctor.create(db, obj_in=doctor_in)
    return doctor


@router.put("/{id}", response_model=schemas.Doctor)
async def update_doctor(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        doctor_in: schemas.DoctorUpdate,
        current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update a doctor.
    """
    doctor = await crud.doctor.get(db, id=id)
    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    doctor = await crud.doctor.update(db, db_obj=doctor, obj_in=doctor_in)
    return doctor


@router.get("/{id}", response_model=schemas.Doctor)
async def read_doctor_by_id(
        id: int,
        db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get a specific doctor by id.
    """
    doctor = await crud.doctor.get(db, id=id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.get("/{doctor_id}/reviews", response_model=List[schemas.Review])
async def read_doctor_reviews(
        doctor_id: int,
        db: AsyncSession = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve reviews for a specific doctor.
    """
    reviews = await crud.review.get_multi_by_doctor(
        db, doctor_id=doctor_id, skip=skip, limit=limit
    )
    return reviews


@router.post("/{doctor_id}/reviews", response_model=schemas.Review)
async def create_doctor_review(
        doctor_id: int,
        review_in: schemas.ReviewCreateForPatient,
        db: AsyncSession = Depends(deps.get_db),
        current_patient: models.User = Depends(deps.get_current_active_patient),
) -> Any:
    """
    Create a new review for a doctor.
    """
    existing_review = await crud.review.get_by_patient_and_doctor(
        db, patient_id=current_patient.id, doctor_id=doctor_id
    )
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this doctor.")

    review = await crud.review.create(db, obj_in=schemas.ReviewCreate(
        **review_in.model_dump(), patient_id=current_patient.id, doctor_id=doctor_id
    ))
    return review
