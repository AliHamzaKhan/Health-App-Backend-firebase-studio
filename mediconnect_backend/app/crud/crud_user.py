from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

from app.core.security import get_password_hash
from app.db.base import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional, List
from app.crud.base import CRUDBase
from app.models import Role


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            phone=obj_in.phone,
            profile_pic=obj_in.profile_pic,
            role_id=obj_in.role_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        result = await db.execute(
            select(User)
            .options(selectinload(User.patient_profile))
            .filter(User.email == email)
        )
        return result.scalars().first()

    async def get_users_by_role(
        self, db: AsyncSession, *, role_name: str, skip: int = 0, limit: int = 100
    ) -> List[User]:
        result = await db.execute(
            select(User)
            .join(Role)
            .filter(Role.role == role_name)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count()).select_from(User))
        return result.scalar_one()


crud_user = CRUDUser(User)
