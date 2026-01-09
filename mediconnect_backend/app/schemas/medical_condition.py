from pydantic import BaseModel

class MedicalConditionBase(BaseModel):
    name: str

class MedicalConditionCreate(MedicalConditionBase):
    pass

class MedicalCondition(MedicalConditionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
