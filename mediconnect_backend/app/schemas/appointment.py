
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time

# Shared properties
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    time: time
    reason: str
    status: str = "UPCOMING"
    notes: Optional[str] = None
    review_given: int = 0


# Properties to receive on appointment creation
class AppointmentCreate(AppointmentBase):
    pass


# Properties to receive on appointment update
class AppointmentUpdate(AppointmentBase):
    pass


# Properties shared by models stored in DB
class AppointmentInDBBase(AppointmentBase):
    id: int
    doctor: 'Doctor'
    patient: 'Patient'
    consultation_details: Optional['Consultation'] = None
    review: Optional['Review'] = None

    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Appointment(AppointmentInDBBase):
    pass


# Properties stored in DB
class AppointmentInDB(AppointmentInDBBase):
    pass

