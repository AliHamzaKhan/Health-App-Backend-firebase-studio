from typing import Any, Dict, Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate

class CRUDAppointment(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):
    async def create_with_patient(self, db: AsyncSession, *, obj_in: AppointmentCreate, patient_id: int) -> Appointment:
        db_obj = self.model(**obj_in.dict(), patient_id=patient_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_patient(
        self, db: AsyncSession, *, patient_id: int, status: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Appointment]:
        query = select(self.model).where(self.model.patient_id == patient_id)
        if status:
            query = query.where(self.model.status == status)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_multi_by_doctor(
        self, db: AsyncSession, *, doctor_id: int, status: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Appointment]:
        query = select(self.model).where(self.model.doctor_id == doctor_id)
        if status:
            query = query.where(self.model.status == status)
        if start_date:
            query = query.where(self.model.date >= start_date)
        if end_date:
            query = query.where(self.model.date <= end_date)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

appointment = CRUDAppointment(Appointment)
