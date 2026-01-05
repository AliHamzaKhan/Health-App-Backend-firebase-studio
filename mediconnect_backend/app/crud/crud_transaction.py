
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any
from sqlalchemy import func
from datetime import datetime

from app.crud.crud_base import CRUDBase
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.db.base import Transaction

class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Transaction]:
        result = await db.execute(
            select(self.model)
            .filter(self.model.patient_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_total_revenue(self, db: AsyncSession) -> float:
        result = await db.execute(
            select(func.sum(self.model.amount))
        )
        total_revenue = result.scalar_one_or_none() or 0.0
        return total_revenue

    async def get_revenue_by_month(self, db: AsyncSession) -> List[Dict[str, Any]]:
        result = await db.execute(
            select(
                func.date_trunc('month', self.model.timestamp).label('month'),
                func.sum(self.model.amount).label('total_revenue')
            )
            .group_by('month')
            .order_by('month')
        )
        return [{'month': row.month.strftime('%B %Y'), 'revenue': row.total_revenue} for row in result.all()]
    
    async def get_transactions(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 10
    ) -> List[Transaction]:
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

crud_transaction = CRUDTransaction(Transaction)
