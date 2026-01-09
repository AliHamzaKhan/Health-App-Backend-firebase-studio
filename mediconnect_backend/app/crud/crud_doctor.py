from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate


class CRUDDoctor(CRUDBase[Doctor, DoctorCreate, DoctorUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[Doctor]:
        result = await db.execute(select(self.model).filter(self.model.email == email))
        return result.scalars().first()

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def get_doctors_by_status(self, db: AsyncSession, *, status: str, skip: int = 0, limit: int = 100) -> List[Doctor]:
        result = await db.execute(select(self.model).filter(self.model.approval_status == status).offset(skip).limit(limit))
        return result.scalars().all()

    async def count_doctors_by_status(self, db: AsyncSession, *, status: str) -> int:
        query = select(func.count()).select_from(self.model).where(self.model.approval_status == status)
        result = await db.execute(query)
        return result.scalar_one()


doctor = CRUDDoctor(Doctor)
