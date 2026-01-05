from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List

from app import models, schemas, crud
from app.api import deps

router = APIRouter()


@router.post("/me/appointments/{appointment_id}/consultation", response_model=schemas.Appointment)
def finalize_consultation(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
    appointment_id: int,
    consultation_in: schemas.ConsultationCreate,
) -> Any:
    """
    Finalizes a scheduled consultation and associates clinical notes.
    """
    appointment = crud.appointment.get(db=db, id=appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this appointment")

    if appointment.status != 'UPCOMING':
        raise HTTPException(status_code=400, detail="Appointment is not in an UPCOMING state")

    updated_appointment = crud.appointment.finalize_consultation(
        db=db, appointment=appointment, consultation_data=consultation_in
    )

    return updated_appointment

@router.post("/me/soap-notes", response_model=schemas.Appointment, status_code=201)
def create_standalone_soap_note(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
    soap_note_in: schemas.StandaloneSoapNoteCreate,
) -> Any:
    """
    Creates a new, standalone clinical record for a patient.
    """
    patient = crud.patient.get(db, id=soap_note_in.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with id {soap_note_in.patient_id} not found")

    # The backend should handle this by creating a new Appointment record
    # that is immediately marked as COMPLETED.
    new_appointment = crud.appointment.create_standalone_soap_note(
        db=db,
        doctor_id=current_user.id,
        soap_note_data=soap_note_in
    )

    return new_appointment

@router.get("/me/patients/{patient_id}/history", response_model=List[schemas.Appointment])
def get_patient_history(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
    patient_id: int,
) -> Any:
    """
    Retrieves the complete clinical history for a specific patient.
    """
    patient = crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with id {patient_id} not found")

    # A check should ideally be in place to ensure the doctor
    # has the right to view the patient's history.
    # For this implementation, we assume any doctor can view any patient's history.

    history = crud.appointment.get_patient_history(db=db, patient_id=patient_id)
    return history
