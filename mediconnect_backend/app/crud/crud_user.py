from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.db.base import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional, List
from app.crud.crud_base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_user_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create_user(self, db: AsyncSession, user: UserCreate):
        from app.core.security import get_password_hash
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def get_all_users(self, db: AsyncSession, email: Optional[str] = None, skip: int = 0, limit: Optional[int] = None) -> List[User]:
        query = select(User)
        if email:
            query = query.filter(User.email.contains(email))
        if limit is not None:
            query = query.offset(skip).limit(limit)
        else:
            query = query.offset(skip)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_users_by_role(self, db: AsyncSession, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        result = await db.execute(select(User).filter(User.role == role).offset(skip).limit(limit))
        return result.scalars().all()

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count()).select_from(User))
        return result.scalar_one()

crud_user = CRUDUser(User)
