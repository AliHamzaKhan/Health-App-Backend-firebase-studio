
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from .appointment import Appointment

# Shared properties
class PatientBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    photo_url: Optional[str] = None
    medical_history: Optional[str] = None

# Properties to receive on patient creation
class PatientCreate(PatientBase):
    pass

# Properties to receive on patient update
class PatientUpdate(PatientBase):
    pass

# Properties shared by models stored in DB
class PatientInDBBase(PatientBase):
    id: int
    appointments: List[Appointment] = []
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Patient(PatientInDBBase):
    pass

# Properties stored in DB
class PatientInDB(PatientInDBBase):
    pass
