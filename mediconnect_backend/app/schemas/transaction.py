from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    appointment_id: int
    amount: int
    transaction_type: str
    timestamp: datetime
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    pass

class TransactionInDBBase(TransactionBase):
    id: int
    patient_id: int
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)

class Transaction(TransactionInDBBase):
    pass
