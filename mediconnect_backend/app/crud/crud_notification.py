from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.crud.crud_base import CRUDBase
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.db.base import Notification
from sqlalchemy import func

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Notification]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_unread_count(self, db: AsyncSession, *, user_id: int) -> int:
        result = await db.execute(
            select(func.count(self.model.id))
            .filter(self.model.user_id == user_id, self.model.is_read == False)
        )
        return result.scalar_one()

    async def mark_as_read(self, db: AsyncSession, *, notification_id: int, user_id: int) -> Optional[Notification]:
        result = await db.execute(select(self.model).filter(self.model.id == notification_id, self.model.user_id == user_id))
        notification = result.scalars().first()
        if notification:
            notification.is_read = True
            await db.commit()
            await db.refresh(notification)
        return notification

crud_notification = CRUDNotification(Notification)