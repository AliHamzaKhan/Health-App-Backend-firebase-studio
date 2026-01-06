from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from app.db.base import Appointment, Notification, User
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.db.session import SessionLocal

async def send_appointment_reminders():
    """
    Sends reminders for appointments scheduled within the next 24 hours.
    """
    async with SessionLocal() as db:
        now = datetime.utcnow()
        twenty_four_hours_later = now + timedelta(hours=24)

        stmt = select(Appointment).where(
            Appointment.status == 'UPCOMING',
            Appointment.time >= now,
            Appointment.time <= twenty_four_hours_later,
            Appointment.reminder_sent == False
        )
        result = await db.execute(stmt)
        appointments = result.scalars().all()

        for appt in appointments:
            # Get patient and doctor users
            patient = await db.get(Patient, appt.patient_id)
            doctor = await db.get(Doctor, appt.doctor_id)
            
            patient_user = await db.get(User, patient.user_id)
            doctor_user = await db.get(User, doctor.user_id)

            # Create notifications
            patient_notification = Notification(
                user_id=patient_user.id,
                message=f"Reminder: You have an appointment with Dr. {doctor_user.full_name} tomorrow at {appt.time.strftime('%H:%M')}."
            )
            doctor_notification = Notification(
                user_id=doctor_user.id,
                message=f"Reminder: You have an appointment with {patient_user.full_name} tomorrow at {appt.time.strftime('%H:%M')}."
            )

            db.add_all([patient_notification, doctor_notification])
            appt.reminder_sent = True


        await db.commit()
