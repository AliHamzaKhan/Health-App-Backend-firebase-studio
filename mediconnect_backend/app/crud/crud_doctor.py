from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models import Doctor, User
from app.schemas.doctor import DoctorCreate, DoctorUpdate

class CRUDDoctor(CRUDBase[Doctor, DoctorCreate, DoctorUpdate]):
    async def get_unverified_doctors_with_documents(self, db: AsyncSession):
        result = await db.execute(
            select(Doctor)
            .join(User)
            .options(selectinload(Doctor.verification_documents), selectinload(Doctor.user))
            .where(User.status == 0) # Assuming 0 is unverified
        )
        return result.scalars().all()

    async def count_doctors_by_status(self, db: AsyncSession, *, status: str) -> int:
        query = (
            select(func.count(self.model.id))
            .join(User, self.model.user_id == User.id)
        )
        if status == "pending":
            query = query.where(User.status == 0)
        elif status == "verified":
             query = query.where(User.status == 1)
        
        total = await db.execute(query)
        return total.scalar_one()

    async def get_doctors_by_status(self, db: AsyncSession, *, status: str, skip: int = 0, limit: int = 100):
        query = (
            select(self.model)
            .join(User, self.model.user_id == User.id)
            .options(joinedload(self.model.user))
        )
        if status == "pending":
            query = query.where(User.status == 0)
        elif status == "verified":
            query = query.where(User.status == 1)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


crud_doctor = CRUDDoctor(Doctor)
