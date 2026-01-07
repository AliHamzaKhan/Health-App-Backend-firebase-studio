from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import func

from app.crud.crud_base import CRUDBase
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.db.base import Review

class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    async def get_multi_by_doctor(
        self, db: AsyncSession, *, doctor_id: int, skip: int = 0, limit: int = 100
    ) -> List[Review]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.doctor_id == doctor_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi_by_patient(
        self, db: AsyncSession, *, patient_id: int, skip: int = 0, limit: int = 100
    ) -> List[Review]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_doctor_average_rating(self, db: AsyncSession, *, doctor_id: int) -> float:
        result = await db.execute(
            select(func.avg(self.model.rating))
            .filter(self.model.doctor_id == doctor_id)
        )
        average_rating = result.scalar_one_or_none()
        return average_rating if average_rating is not None else 0.0

    async def get_by_patient_and_doctor(self, db: AsyncSession, *, patient_id: int, doctor_id: int) -> Review | None:
        result = await db.execute(
            select(self.model)
            .filter(self.model.patient_id == patient_id, self.model.doctor_id == doctor_id)
        )
        return result.scalars().first()

crud_review = CRUDReview(Review)
