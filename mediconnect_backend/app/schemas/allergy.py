from pydantic import BaseModel

class AllergyBase(BaseModel):
    name: str

class AllergyCreate(AllergyBase):
    pass

class AllergyUpdate(AllergyBase):
    pass

class Allergy(AllergyBase):
    id: int

    class Config:
        orm_mode = True
