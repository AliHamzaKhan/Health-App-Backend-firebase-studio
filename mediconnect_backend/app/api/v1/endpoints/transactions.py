from fastapi import APIRouter, Depends, Query, Response, UploadFile, File, HTTPException
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import deps
from app.crud.crud_transaction import crud_transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, Transaction
from app.db.base import User

router = APIRouter()

@router.get("/transactions")
async def get_transactions(page: int = 1, size: int = 10, db: AsyncSession = Depends(deps.get_db)):
    skip = (page - 1) * size
    transactions = await crud_transaction.get_multi(db, skip=skip, limit=size)
    total_transactions = len(transactions)
    return {"total": total_transactions, "page": page, "size": size, "transactions": transactions}

@router.post("/transactions", response_model=Transaction)
async def create_transaction(
    *,
    db: AsyncSession = Depends(deps.get_db),
    transaction_in: TransactionCreate
):
    """
    Create new transaction.
    """
    transaction = await crud_transaction.create(db, obj_in=transaction_in)
    return transaction

@router.get("/transactions/user", response_model=List[Transaction])
async def get_transactions_by_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    page: int = 1,
    size: int = 10,
):
    """
    Get transactions for current user.
    """
    skip = (page - 1) * size
    transactions = await crud_transaction.get_by_user(db, user_id=current_user.id, skip=skip, limit=size)
    return transactions

@router.get("/transactions/{id}", response_model=Transaction)
async def get_transaction(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    """
    Get transaction by ID.
    """
    transaction = await crud_transaction.get(db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/transactions/{id}", response_model=Transaction)
async def update_transaction(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    transaction_in: TransactionUpdate
):
    """
    Update transaction.
    """
    transaction = await crud_transaction.get(db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction = await crud_transaction.update(db, db_obj=transaction, obj_in=transaction_in)
    return transaction

@router.delete("/transactions/{id}", response_model=Transaction)
async def delete_transaction(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int
):
    """
    Delete transaction.
    """
    transaction = await crud_transaction.get(db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction = await crud_transaction.remove(db, id=id)
    return transaction
