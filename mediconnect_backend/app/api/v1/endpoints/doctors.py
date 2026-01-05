from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Doctor])
def read_doctors(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve doctors.
    """
    if crud.user.is_superuser(current_user):
        doctors = crud.doctor.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return doctors


@router.post("/register", response_model=schemas.Doctor)
def register_doctor(
    *,
    db: Session = Depends(deps.get_db),
    doctor_in: schemas.DoctorCreate,
) -> Any:
    """
    Create new doctor.
    """
    doctor = crud.doctor.get_by_email(db, email=doctor_in.email)
    if doctor:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    doctor = crud.doctor.create(db, obj_in=doctor_in)
    return doctor


@router.post("/", response_model=schemas.Doctor)
def create_doctor(
    *, 
    db: Session = Depends(deps.get_db),
    doctor_in: schemas.DoctorCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new doctor.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    doctor = crud.doctor.get_by_email(db, email=doctor_in.email)
    if doctor:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    doctor = crud.doctor.create(db, obj_in=doctor_in)
    return doctor


@router.put("/{id}", response_model=schemas.Doctor)
def update_doctor(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    doctor_in: schemas.DoctorUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a doctor.
    """
    doctor = crud.doctor.get(db, id=id)
    if not doctor:
        raise HTTPException(
            status_code=44,
            detail="The user with this username does not exist in the system",
        )
    doctor = crud.doctor.update(db, db_obj=doctor, obj_in=doctor_in)
    return doctor


@router.get("/{id}", response_model=schemas.Doctor)
def read_doctor_by_id(
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific doctor by id.
    """
    doctor = crud.doctor.get(db, id=id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.get("/me/dashboard-stats", response_model=schemas.DoctorDashboardStats)
def get_dashboard_stats(
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Fetches all key performance indicators (KPIs) and recent data for the main doctor dashboard.
    """
    # This is a placeholder implementation. 
    return {
        "todaysAppointments": 5,
        "totalPatients": 120,
        "thisMonthsIncome": 4500.50,
        "pendingReports": 3
    }

@router.get("/me/profile", response_model=schemas.Doctor)
def get_doctor_profile(
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Fetches the complete, detailed profile for the currently logged-in doctor.
    """
    return current_user

@router.put("/me/profile", response_model=schemas.Doctor)
def update_doctor_profile(
    *,
    db: Session = Depends(deps.get_db),
    doctor_in: schemas.DoctorUpdate,
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Updates the profile of the currently logged-in doctor.
    """
    doctor = crud.doctor.update(db, db_obj=current_user, obj_in=doctor_in)
    return doctor

@router.post("/me/documents")
async def upload_doctor_documents(
    license: UploadFile = File(...), 
    degree: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_doctor),
):
    """
    Allows a newly registered doctor to upload their medical license and degree certificate for verification.
    """
    # In a real application, you would save these files and update the doctor's verification status.
    return {"message": "Documents uploaded successfully"}

@router.get("/me/verification-status")
def get_verification_status(
    current_user: models.User = Depends(deps.get_current_active_doctor),
):
    """
    Allows a doctor to check their current verification status (`pending`, `approved`, `rejected`).
    """
    # This is a placeholder. In a real app, you'd fetch this from the database.
    return {"verification_status": "pending"}

@router.get("/me/appointments", response_model=List[schemas.Appointment])
def get_doctor_appointments(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Retrieves a list of all appointments for the logged-in doctor.
    """
    appointments = crud.appointment.get_multi_by_doctor(db, doctor_id=current_user.id)
    return appointments

@router.get("/me/appointments/{appointment_id}", response_model=schemas.Appointment)
def get_doctor_appointment(
    appointment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Retrieves the details of a single appointment.
    """
    appointment = crud.appointment.get(db, id=appointment_id)
    if not appointment or appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.patch("/me/appointments/{appointment_id}", response_model=schemas.Appointment)
def update_doctor_appointment(
    appointment_id: int,
    appointment_in: schemas.AppointmentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Allows a doctor to cancel or reschedule an appointment.
    """
    appointment = crud.appointment.get(db, id=appointment_id)
    if not appointment or appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment = crud.appointment.update(db, db_obj=appointment, obj_in=appointment_in)
    return appointment

@router.post("/me/appointments/{appointment_id}/consultation", response_model=schemas.Consultation)
def finalize_consultation(
    appointment_id: int,
    consultation_in: schemas.ConsultationCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Finalizes a consultation, submitting all details.
    """
    appointment = crud.appointment.get(db, id=appointment_id)
    if not appointment or appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    consultation = crud.consultation.create_with_appointment(
        db, obj_in=consultation_in, appointment_id=appointment_id
    )
    return consultation

@router.get("/me/patients", response_model=List[schemas.Patient])
def get_doctor_patients(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Retrieves a list of all unique patients associated with the doctor.
    """
    patients = crud.patient.get_multi_by_doctor(db, doctor_id=current_user.id)
    return patients

@router.get("/me/patients/{patient_id}/history")
def get_patient_history(
    patient_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
):
    """
    Retrieves a specific patient's complete history.
    """
    # This would involve a more complex query in a real application
    appointments = crud.appointment.get_multi_by_patient_and_doctor(
        db, patient_id=patient_id, doctor_id=current_user.id
    )
    return appointments


@router.post("/me/patients", response_model=schemas.Patient)
def create_patient(
    patient_in: schemas.PatientCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Manually creates a new patient record in the system.
    """
    patient = crud.patient.create_with_doctor(db, obj_in=patient_in, doctor_id=current_user.id)
    return patient

@router.post("/me/soap-notes", response_model=schemas.SoapNote)
def create_soap_note(
    soap_note_in: schemas.SoapNoteCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Creates a standalone SOAP note for a patient.
    """
    soap_note = crud.soap_note.create_with_doctor(
        db, obj_in=soap_note_in, doctor_id=current_user.id
    )
    return soap_note

@router.get("/me/hospital-schedules", response_model=List[schemas.HospitalSchedule])
def get_hospital_schedules(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Lists all hospital schedules for the doctor.
    """
    schedules = crud.hospital_schedule.get_multi_by_doctor(db, doctor_id=current_user.id)
    return schedules

@router.post("/me/hospital-schedules", response_model=schemas.HospitalSchedule)
def create_hospital_schedule(
    schedule_in: schemas.HospitalScheduleCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Creates a new hospital schedule.
    """
    schedule = crud.hospital_schedule.create_with_doctor(
        db, obj_in=schedule_in, doctor_id=current_user.id
    )
    return schedule

@router.put("/me/hospital-schedules/{schedule_id}", response_model=schemas.HospitalSchedule)
def update_hospital_schedule(
    schedule_id: int,
    schedule_in: schemas.HospitalScheduleUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Updates a hospital schedule.
    """
    schedule = crud.hospital_schedule.get(db, id=schedule_id)
    if not schedule or schedule.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail="Schedule not found")
    schedule = crud.hospital_schedule.update(db, db_obj=schedule, obj_in=schedule_in)
    return schedule

@router.delete("/me/hospital-schedules/{schedule_id}", response_model=schemas.HospitalSchedule)
def delete_hospital_schedule(
    schedule_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Deletes a hospital schedule.
    """
    schedule = crud.hospital_schedule.get(db, id=schedule_id)
    if not schedule or schedule.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail="Schedule not found")
    crud.hospital_schedule.remove(db, id=schedule_id)
    return schedule

@router.get("/me/income/stats")
def get_income_stats(
    current_user: models.User = Depends(deps.get_current_active_doctor),
):
    """
    Retrieves key financial metrics.
    """
    # Placeholder
    return {"total_income": 10000, "monthly_income": 2000}

@router.get("/me/income/chart-data")
def get_income_chart_data(
    current_user: models.User = Depends(deps.get_current_active_doctor),
):
    """
    Retrieves data formatted for revenue charts.
    """
    # Placeholder
    return {"labels": ["Jan", "Feb", "Mar"], "data": [1000, 1200, 1500]}

@router.get("/me/income/transactions", response_model=List[schemas.Transaction])
def get_income_transactions(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
) -> Any:
    """
    Retrieves a list of recent financial transactions.
    """
    transactions = crud.transaction.get_multi_by_user(db, user_id=current_user.id)
    return transactions

@router.get("/subscriptions/plans/doctor", response_model=List[schemas.Subscription])
def get_doctor_subscription_plans(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieves all available subscription plans for doctors.
    """
    # This is a placeholder. You'd fetch plans specifically for doctors.
    return crud.subscription.get_multi(db)

@router.post("/subscriptions/purchase", response_model=schemas.Transaction)
def purchase_subscription(
    plan_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_doctor),
):
    """
    Handles the purchase of a recurring subscription.
    """
    # This is a placeholder for a complex billing integration.
    subscription_plan = crud.subscription.get(db, id=plan_id)
    if not subscription_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Create a transaction record
    transaction_in = schemas.TransactionCreate(
        amount=subscription_plan.price, 
        user_id=current_user.id, 
        status="completed"
    )
    transaction = crud.transaction.create(db, obj_in=transaction_in)
    return transaction
