from pydantic import BaseModel, ConfigDict
from typing import Dict

class HospitalScheduleBase(BaseModel):
    consultationFee: float
    availability: Dict

class HospitalScheduleCreate(HospitalScheduleBase):
    hospital_id: int
    doctor_id: int

class HospitalScheduleUpdate(HospitalScheduleBase):
    pass

class HospitalScheduleInDBBase(HospitalScheduleBase):
    id: int
    hospital_id: int
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)

class HospitalSchedule(HospitalScheduleInDBBase):
    pass
