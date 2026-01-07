from app.crud.crud_base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, Permission as PermissionSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionSchema]):
    async def get_by_role(self, db: AsyncSession, *, role: str) -> Permission:
        result = await db.execute(select(self.model).filter(self.model.role == role))
        return result.scalars().first()

    async def get_multi_by_type(
        self, db: AsyncSession, *, type: str, skip: int = 0, limit: int = 100
    ) -> List[Permission]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.type == type)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

permission = CRUDPermission(Permission)
