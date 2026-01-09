from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import User

class DoctorBase(BaseModel):
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    bio: Optional[str] = None
    office_address: Optional[str] = None
    office_hours: Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    pass

class DoctorInDBBase(DoctorBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Doctor(DoctorInDBBase):
    pass

class DoctorVerificationDocument(BaseModel):
    id: int
    doctor_id: int
    document_type: str
    document_url: str
    is_verified: bool

    class Config:
        from_attributes = True

class DoctorWithVerificationInfo(Doctor):
    user: User
    verification_documents: List[DoctorVerificationDocument]
