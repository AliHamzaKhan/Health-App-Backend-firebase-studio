from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_subscription import subscription as crud_subscription
from app.schemas.subscription import Subscription, SubscriptionCreate, SubscriptionUpdate
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Subscription)
async def create_subscription(
    *,
    db: AsyncSession = Depends(deps.get_db),
    subscription_in: SubscriptionCreate,
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Create new subscription.
    """
    subscription = await crud_subscription.get_by_name(db, name=subscription_in.name)
    if subscription:
        raise HTTPException(
            status_code=400,
            detail="The subscription with this name already exists in the system.",
        )
    subscription = await crud_subscription.create(db, obj_in=subscription_in)
    return subscription


@router.get("/{subscription_id}", response_model=Subscription)
async def read_subscription(
    *,
    db: AsyncSession = Depends(deps.get_db),
    subscription_id: int,
):
    """
    Get subscription by ID.
    """
    subscription = await crud_subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="The subscription with this ID does not exist in the system.",
        )
    return subscription


@router.get("/", response_model=List[Subscription])
async def read_subscriptions(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve subscriptions.
    """
    subscriptions = await crud_subscription.get_multi(db, skip=skip, limit=limit)
    return subscriptions


@router.put("/{subscription_id}", response_model=Subscription)
async def update_subscription(
    *,
    db: AsyncSession = Depends(deps.get_db),
    subscription_id: int,
    subscription_in: SubscriptionUpdate,
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Update a subscription.
    """
    subscription = await crud_subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="The subscription with this ID does not exist in the system.",
        )
    subscription = await crud_subscription.update(db, db_obj=subscription, obj_in=subscription_in)
    return subscription


@router.delete("/{subscription_id}", response_model=Subscription)
async def delete_subscription(
    *,
    db: AsyncSession = Depends(deps.get_db),
    subscription_id: int,
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Delete a subscription.
    """
    subscription = await crud_subscription.get(db, id=subscription_id)
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="The subscription with this ID does not exist in the system.",
        )
    subscription = await crud_subscription.remove(db, id=subscription_id)
    return subscription