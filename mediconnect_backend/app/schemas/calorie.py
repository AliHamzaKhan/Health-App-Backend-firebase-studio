from pydantic import BaseModel

class CalorieBase(BaseModel):
    name: str
    calories: int

class CalorieCreate(CalorieBase):
    pass

class CalorieUpdate(CalorieBase):
    pass

class Calorie(CalorieBase):
    id: int

    class Config:
        orm_mode = True
