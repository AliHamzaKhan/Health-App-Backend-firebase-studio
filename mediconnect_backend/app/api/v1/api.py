from fastapi import APIRouter

from app.api.v1.endpoints import (auth, admin, appointments, consultations, transactions, reviews, notifications, patients, doctors, medications, permissions, ai, symptoms, allergies, calories)

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])

api_router.include_router(
    admin.router, 
    prefix="/admin", 
    tags=["admin"]
)
api_router.include_router(
    permissions.router, 
    prefix="/admin/permissions", 
    tags=["permissions"]
)

api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(consultations.router, prefix="/consultations", tags=["consultations"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
api_router.include_router(medications.router, prefix="/medications", tags=["medications"])
api_router.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"])
api_router.include_router(allergies.router, prefix="/allergies", tags=["allergies"])
api_router.include_router(calories.router, prefix="/calories", tags=["calories"])
