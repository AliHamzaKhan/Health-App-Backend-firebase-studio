from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api.v1 import deps
from app.crud import crud_appointment
from app.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate
from app.models.user import User
from app.schemas.consultation import ConsultationCreate
from app.schemas.response import StandardResponse

router = APIRouter()

@router.get("/patients/me/appointments", response_model=StandardResponse[List[Appointment]])
async def read_patient_appointments(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    status: Optional[str] = None,
):
    """
    Retrieve appointments for the current patient.
    """
    if current_user.role != 5:
        return StandardResponse(success=False, message="Not authorized to access this resource")
    appointments = await crud_appointment.get_multi_by_patient(db, patient_id=current_user.id, status=status)
    return StandardResponse(data=appointments, message="Patient appointments retrieved successfully.")


@router.post("/patients/me/appointments", response_model=StandardResponse[Appointment])
async def create_patient_appointment(
    *,
    db: AsyncSession = Depends(deps.get_db),
    appointment_in: AppointmentCreate,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Create a new appointment for the current patient.
    """
    if current_user.role != 5:
        return StandardResponse(success=False, message="Not authorized to perform this action")
    appointment = await crud_appointment.create_with_patient(db, obj_in=appointment_in, patient_id=current_user.id)
    return StandardResponse(data=appointment, message="Appointment created successfully.")


@router.get("/patients/me/appointments/{appointment_id}", response_model=StandardResponse[Appointment])
async def read_patient_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Get a specific appointment for the current patient.
    """
    appointment = await crud_appointment.get(db, id=appointment_id)
    if not appointment or appointment.patient_id != current_user.id:
        return StandardResponse(success=False, message="Appointment not found")
    return StandardResponse(data=appointment, message="Appointment retrieved successfully.")


@router.patch("/patients/me/appointments/{appointment_id}", response_model=StandardResponse[Appointment])
async def cancel_patient_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Cancel an appointment for the current patient.
    """
    appointment = await crud_appointment.get(db, id=appointment_id)
    if not appointment or appointment.patient_id != current_user.id:
        return StandardResponse(success=False, message="Appointment not found")
    
    update_data = {"status": "CANCELLED"}
    updated_appointment = await crud_appointment.update(db, db_obj=appointment, obj_in=update_data)
    return StandardResponse(data=updated_appointment, message="Appointment cancelled successfully.")


@router.get("/doctors/me/appointments", response_model=StandardResponse[List[Appointment]])
async def read_doctor_appointments(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    status: Optional[str] = None,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve appointments for the current doctor.
    """
    if current_user.role != 3:
        return StandardResponse(success=False, message="Not authorized to access this resource")
    appointments = await crud_appointment.get_multi_by_doctor(
        db, doctor_id=current_user.id, status=status, start_date=startDate, end_date=endDate, skip=skip, limit=limit
    )
    return StandardResponse(data=appointments, message="Doctor appointments retrieved successfully.")


@router.get("/doctors/me/appointments/{appointment_id}", response_model=StandardResponse[Appointment])
async def read_doctor_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Get a specific appointment for the current doctor.
    """
    appointment = await crud_appointment.get(db, id=appointment_id)
    if not appointment or appointment.doctor_id != current_user.id:
        return StandardResponse(success=False, message="Appointment not found")
    return StandardResponse(data=appointment, message="Appointment retrieved successfully.")


@router.patch("/doctors/me/appointments/{appointment_id}", response_model=StandardResponse[Appointment])
async def update_doctor_appointment(
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Update an appointment for the current doctor.
    """
    appointment = await crud_appointment.get(db, id=appointment_id)
    if not appointment or appointment.doctor_id != current_user.id:
        return StandardResponse(success=False, message="Appointment not found")

    updated_appointment = await crud_appointment.update(db, db_obj=appointment, obj_in=appointment_in)
    return StandardResponse(data=updated_appointment, message="Appointment updated successfully.")


@router.post("/doctors/me/appointments/{appointment_id}/consultation", response_model=StandardResponse[Appointment])
async def create_consultation_for_appointment(
    appointment_id: int,
    consultation_in: ConsultationCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Create a consultation for a specific appointment.
    """
    if current_user.role != 3:
        return StandardResponse(success=False, message="Not authorized")

    appointment = await crud_appointment.get(db, id=appointment_id)
    if not appointment or appointment.doctor_id != current_user.id:
        return StandardResponse(success=False, message="Appointment not found")

    # This is a placeholder for where you'd create the consultation and link it to the appointment
    # For now, we'll just update the appointment status
    update_data = {"status": "COMPLETED"}
    updated_appointment = await crud_appointment.update(db, db_obj=appointment, obj_in=update_data)
    return StandardResponse(data=updated_appointment, message="Consultation created and appointment status updated successfully.")

@router.post("/doctors/me/appointments/follow-up", response_model=StandardResponse[Appointment])
async def create_follow_up_appointment(
    appointment_in: AppointmentCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Create a follow-up appointment for a patient.
    """
    if current_user.role != 3:
        return StandardResponse(success=False, message="Not authorized to perform this action")
    
    # The doctor creates an appointment on behalf of a patient.
    # The `appointment_in` schema should contain the patient_id.
    appointment = await crud_appointment.create(db, obj_in=appointment_in)
    return StandardResponse(data=appointment, message="Follow-up appointment created successfully.")
