
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class MedicationBase(BaseModel):
    name: str
    description: Optional[str] = None

class MedicationCreate(MedicationBase):
    pass

class MedicationUpdate(MedicationBase):
    pass

class Medication(MedicationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PrescribedMedicineBase(BaseModel):
    name: str
    dosage: str
    frequency: str

class PrescribedMedicineCreate(PrescribedMedicineBase):
    pass

class PrescribedMedicine(PrescribedMedicineBase):
    id: int
    consultation_id: int
    model_config = ConfigDict(from_attributes=True)
