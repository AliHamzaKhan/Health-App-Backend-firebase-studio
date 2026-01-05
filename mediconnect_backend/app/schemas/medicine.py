
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class MedicineBase(BaseModel):
    name: str
    description: Optional[str] = None

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(MedicineBase):
    pass

class Medicine(MedicineBase):
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
