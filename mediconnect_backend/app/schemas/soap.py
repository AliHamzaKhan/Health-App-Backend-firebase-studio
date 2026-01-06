from pydantic import BaseModel

class SoapNoteBase(BaseModel):
    note: str
    patient_id: int

class SoapNoteCreate(SoapNoteBase):
    pass

class SoapNote(SoapNoteBase):
    id: int

    class Config:
        orm_mode = True
