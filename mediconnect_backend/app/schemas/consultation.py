
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .medicine import PrescribedMedicine

# Shared properties
class ConsultationBase(BaseModel):
    hpi: str
    soap_note: str
    icd_codes: str
    treatment_plan: str
    referral: Optional[str] = None
    recommended_lab_tests: Optional[List[str]] = []


# Properties to receive on consultation creation
class ConsultationCreate(ConsultationBase):
    prescribed_medicines: Optional[List[str]] = []

# Properties to receive on consultation update
class ConsultationUpdate(ConsultationBase):
    pass


# Properties shared by models stored in DB
class ConsultationInDBBase(ConsultationBase):
    id: int
    appointment_id: int
    prescribed_medicines: List[PrescribedMedicine] = []

    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Consultation(ConsultationInDBBase):
    pass


# Properties stored in DB
class ConsultationInDB(ConsultationInDBBase):
    pass
