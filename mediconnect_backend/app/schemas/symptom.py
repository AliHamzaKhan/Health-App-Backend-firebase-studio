


from pydantic import BaseModel, ConfigDict

class SymptomBase(BaseModel):
    name: str

class SymptomCreate(SymptomBase):
    pass

class SymptomUpdate(SymptomBase):
    pass

class Symptom(SymptomBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
