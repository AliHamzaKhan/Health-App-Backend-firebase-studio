from pydantic import BaseModel, ConfigDict
from typing import List, Dict

class HospitalBase(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    departments: str
    website: str
    phone_no: str
    current_status: str
    image: str
    timings: str

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdate(HospitalBase):
    pass

class HospitalInDBBase(HospitalBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Hospital(HospitalInDBBase):
    pass
