from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_notification import crud_notification
from app.schemas.notification import NotificationCreate, NotificationUpdate, Notification
from app.db.base import User
from app.schemas.response import StandardResponse

router = APIRouter()

@router.post("/notifications", response_model=StandardResponse[Notification])
async def create_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    notification_in: NotificationCreate
):
    notification = await crud_notification.create(db, obj_in=notification_in)
    return StandardResponse(data=notification, message="Notification created successfully.")

@router.get("/notifications/{id}", response_model=StandardResponse[Notification])
async def get_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    notification = await crud_notification.get(db, id=id)
    if not notification:
        return StandardResponse(success=False, message="Notification not found")
    return StandardResponse(data=notification, message="Notification retrieved successfully.")

@router.get("/notifications", response_model=StandardResponse[List[Notification]])
async def get_all_notifications(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    notifications = await crud_notification.get_multi(db, user_id=current_user.id)
    return StandardResponse(data=notifications, message="Notifications retrieved successfully.")

@router.put("/notifications/{id}", response_model=StandardResponse[Notification])
async def update_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    notification_in: NotificationUpdate
):
    notification = await crud_notification.get(db, id=id)
    if not notification:
        return StandardResponse(success=False, message="Notification not found")
    notification = await crud_notification.update(db, db_obj=notification, obj_in=notification_in)
    return StandardResponse(data=notification, message="Notification updated successfully.")

@router.delete("/notifications/{id}", response_model=StandardResponse[Notification])
async def delete_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    notification = await crud_notification.get(db, id=id)
    if not notification:
        return StandardResponse(success=False, message="Notification not found")
    notification = await crud_notification.remove(db, id=id)
    return StandardResponse(data=notification, message="Notification deleted successfully.")
