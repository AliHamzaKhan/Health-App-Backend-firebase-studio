from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# Shared properties
class DoctorBase(BaseModel):
    name: str
    email: str
    specialty: str
    phone_number: Optional[str] = None
    is_active: bool = True
    photo_url: Optional[str] = None


# Properties to receive on doctor creation
class DoctorCreate(DoctorBase):
    pass


# Properties to receive on doctor update
class DoctorUpdate(DoctorBase):
    pass


# Properties shared by models stored in DB
class DoctorInDBBase(DoctorBase):
    id: int
    appointments: List['Appointment'] = []
    reviews: List['Review'] = []
    schedules: List['Schedule'] = []
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Doctor(DoctorInDBBase):
    pass


# Properties stored in DB
class DoctorInDB(DoctorInDBBase):
    pass


class DoctorDashboardStats(BaseModel):
    total_patients: int
    upcoming_appointments: int
    total_revenue: float
