from pydantic import BaseModel
from datetime import date, time

class ScheduleBase(BaseModel):
    doctor_id: int
    date: date
    start_time: time
    end_time: time

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    is_available: bool

    class Config:
        from_orm = True
