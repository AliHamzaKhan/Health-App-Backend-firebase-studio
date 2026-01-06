
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.schemas.subscription import SubscriptionPurchase

router = APIRouter()


@router.get("/", response_model=List[schemas.Patient])
def read_patients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve patients.
    """
    if crud.user.is_superuser(current_user):
        patients = crud.patient.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return patients


@router.post("/register", response_model=schemas.Patient)
def register_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_in: schemas.PatientCreate,
) -> Any:
    """
    Create new patient.
    """
    patient = crud.patient.get_by_email(db, email=patient_in.email)
    if patient:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    patient = crud.patient.create(db, obj_in=patient_in)
    return patient


@router.post("/", response_model=schemas.Patient)
def create_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_in: schemas.PatientCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new patient.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    patient = crud.patient.get_by_email(db, email=patient_in.email)
    if patient:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    patient = crud.patient.create(db, obj_in=patient_in)
    return patient


@router.put("/{id}", response_model=schemas.Patient)
def update_patient(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    patient_in: schemas.PatientUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a patient.
    """
    patient = crud.patient.get(db, id=id)
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    patient = crud.patient.update(db, db_obj=patient, obj_in=patient_in)
    return patient


@router.get("/{id}", response_model=schemas.Patient)
def read_patient_by_id(
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific patient by id.
    """
    patient = crud.patient.get(db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/me/tokens", response_model=int)
def read_patient_tokens(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current token count.
    """
    # This is a mock response
    return 10


@router.get("/subscriptions/plans", response_model=List[dict])
def read_subscription_plans() -> Any:
    """
    Get all subscription plans.
    """
    # This is a mock response
    return [
        {"id": "plan_1", "name": "Basic", "price": 10},
        {"id": "plan_2", "name": "Premium", "price": 20},
    ]


@router.post("/subscriptions/purchase")
def purchase_subscription(
    *,
    db: Session = Depends(deps.get_db),
    purchase_in: SubscriptionPurchase,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Purchase a subscription or a token package.
    """
    # This is a mock response
    return {"status": "success", "message": f"Purchased {purchase_in.type} with id {purchase_in.planId}"}


@router.get("/me/subscription", response_model=dict)
def read_patient_subscription(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current subscription.
    """
    # This is a mock response
    return {"id": "sub_1", "plan_id": "plan_1", "status": "active"}


@router.get("/me/appointments", response_model=List[schemas.Appointment])
def get_patient_appointments(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    status: str = None,
) -> Any:
    """
    Retrieves a list of the patient's own appointments.
    """
    appointments = crud.appointment.get_multi_by_patient(
        db, patient_id=current_user.id, status=status
    )
    return appointments


@router.post("/me/appointments", response_model=schemas.Appointment)
def book_appointment(
    *,
    db: Session = Depends(deps.get_db),
    appointment_in: schemas.AppointmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Books a new appointment with a specified doctor.
    """
    appointment = crud.appointment.create_with_patient(
        db, obj_in=appointment_in, patient_id=current_user.id
    )
    return appointment


@router.get("/me/appointments/{appointment_id}", response_model=schemas.Appointment)
def get_patient_appointment(
    appointment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves the full details of a single appointment.
    """
    appointment = crud.appointment.get(db, id=appointment_id)
    if not appointment or appointment.patient_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/me/appointments/{appointment_id}", response_model=schemas.Appointment)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Allows the patient to cancel their upcoming appointment.
    """
    appointment = crud.appointment.get(db, id=appointment_id)
    if not appointment or appointment.patient_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.status != "UPCOMING":
        raise HTTPException(status_code=400, detail="Only upcoming appointments can be cancelled")

    appointment_in = schemas.AppointmentUpdate(status="CANCELLED")
    appointment = crud.appointment.update(db, db_obj=appointment, obj_in=appointment_in)
    return appointment
