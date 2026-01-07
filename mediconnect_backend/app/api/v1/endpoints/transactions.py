from fastapi import APIRouter, Depends
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_transaction import crud_transaction
from app.schemas.transaction import Transaction
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Transaction])
async def read_transactions(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve transactions.
    """
    transactions = await crud_transaction.get_transactions(db, skip=skip, limit=limit)
    return transactions


@router.get("/user/{user_id}", response_model=List[Transaction])
async def read_transactions_by_user(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve transactions for a specific user.
    """
    transactions = await crud_transaction.get_by_user(
        db, user_id=user_id, skip=skip, limit=limit
    )
    return transactions


@router.get("/revenue", response_model=float)
async def get_total_revenue(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Get total revenue.
    """
    total_revenue = await crud_transaction.get_total_revenue(db)
    return total_revenue


@router.get("/revenue/by-month", response_model=List[dict])
async def get_revenue_by_month(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Get revenue by month.
    """
    revenue_by_month = await crud_transaction.get_revenue_by_month(db)
    return revenue_by_month
