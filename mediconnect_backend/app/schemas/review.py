from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    doctor_id: int
    patient_id: int

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
