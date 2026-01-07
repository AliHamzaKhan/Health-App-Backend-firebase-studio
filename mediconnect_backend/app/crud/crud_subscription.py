from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.crud.crud_base import CRUDBase
from app.db.base import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate

class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Subscription]:
        result = await db.execute(select(self.model).filter(self.model.name == name))
        return result.scalars().first()

subscription = CRUDSubscription(Subscription)
