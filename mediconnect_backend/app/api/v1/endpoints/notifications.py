from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_notification import crud_notification
from app.schemas.notification import NotificationCreate, NotificationUpdate, Notification
from app.db.base import User

router = APIRouter()

@router.post("/notifications", response_model=Notification)
async def create_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    notification_in: NotificationCreate
):
    notification = await crud_notification.create(db, obj_in=notification_in)
    return notification

@router.get("/notifications/{id}", response_model=Notification)
async def get_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    notification = await crud_notification.get(db, id=id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.get("/notifications", response_model=List[Notification])
async def get_all_notifications(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return await crud_notification.get_multi(db, user_id=current_user.id)

@router.put("/notifications/{id}", response_model=Notification)
async def update_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    notification_in: NotificationUpdate
):
    notification = await crud_notification.get(db, id=id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification = await crud_notification.update(db, db_obj=notification, obj_in=notification_in)
    return notification

@router.delete("/notifications/{id}", response_model=Notification)
async def delete_notification(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    notification = await crud_notification.get(db, id=id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification = await crud_notification.remove(db, id=id)
    return notification
