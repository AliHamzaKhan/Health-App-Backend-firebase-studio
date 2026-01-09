from pydantic import BaseModel
from typing import Optional

class VitalBase(BaseModel):
    name: str
    value: str
    unit: Optional[str] = None

class VitalCreate(VitalBase):
    pass

class VitalUpdate(VitalBase):
    pass

class Vital(VitalBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True
