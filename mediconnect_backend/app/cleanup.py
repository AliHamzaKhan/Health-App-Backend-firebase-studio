from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from sqlalchemy import delete

from app.db.base import Appointment, Notification
from app.db.session import SessionLocal

async def cleanup_old_appointments():
    """
    Deletes appointments that are older than one year and have a status of
    'COMPLETED' or 'CANCELLED'.
    """
    async with SessionLocal() as db:
        one_year_ago = datetime.utcnow() - timedelta(days=365)

        stmt = delete(Appointment).where(
            Appointment.date < one_year_ago,
            Appointment.status.in_(['COMPLETED', 'CANCELLED'])
        )
        await db.execute(stmt)
        await db.commit()

async def cleanup_old_notifications():
    """
    Deletes notifications that are older than 90 days.
    """
    async with SessionLocal() as db:
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        stmt = delete(Notification).where(Notification.created_at < ninety_days_ago)
        await db.execute(stmt)
        await db.commit()
