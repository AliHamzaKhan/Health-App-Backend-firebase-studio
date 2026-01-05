from pydantic import BaseModel, Field
from typing import Optional, List

class Report(BaseModel):
    title: str
    patient_id: int
    summary: str
    recommendations: str

class ReportSummary(BaseModel):
    title: str
    summary: str
    patient_id: int

class SoapNoteGenerationResponse(BaseModel):
    soap_note: str

class AIModelBase(BaseModel):
    name: str
    description: str
    price: int

class AIModelCreate(AIModelBase):
    pass

class AIModel(AIModelBase):
    id: int

    class Config:
        orm_mode = True
