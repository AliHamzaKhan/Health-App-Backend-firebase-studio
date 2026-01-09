from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.cleanup import cleanup_old_appointments, cleanup_old_notifications
from app.reminders import send_appointment_reminders

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

scheduler = AsyncIOScheduler()

def initialize_database():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    initialize_database()
    scheduler.add_job(cleanup_old_appointments, 'interval', days=1)
    scheduler.add_job(cleanup_old_notifications, 'interval', days=1)
    scheduler.add_job(send_appointment_reminders, 'interval', hours=1)
    scheduler.start()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
