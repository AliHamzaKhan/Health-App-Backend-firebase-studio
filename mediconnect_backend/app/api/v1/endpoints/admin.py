from fastapi import APIRouter, Depends, Query, Response, UploadFile, File, HTTPException
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import io
from starlette.responses import StreamingResponse

from app.api.v1 import deps
from app.api.v1.deps import get_current_active_admin
from app.crud.crud_user import crud_user
from app.crud.crud_hospital import hospital as crud_hospital
from app.crud.crud_medication import crud_medication
from app.crud.crud_notification import crud_notification
from app.crud.crud_transaction import crud_transaction
from app.crud import crud_doctor
from app.models.doctor import Doctor
from app.models.user import User
from app.models.hospital import Hospital
from app.models.medication import Medication
from app.schemas.doctor import DoctorUpdate
from app.schemas.user import UserUpdate
from app.schemas.hospital import HospitalCreate, HospitalUpdate
from app.schemas.medication import MedicationCreate, MedicationUpdate
from app.schemas.notification import NotificationCreate, NotificationBroadcast

router = APIRouter()

@router.get("/dashboard-stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user=Depends(get_current_active_admin)
):
    """
    Fetches all key performance indicators (KPIs) and recent data needed for the main dashboard view.
    """
    total_users = len(await crud_user.get_all_users(db))
    total_doctors = len(await crud_doctor.get_all_doctors(db))
    pending_doctor_approvals = await crud_doctor.count_doctors_by_status(db, status="pending")
    total_hospitals = len(await crud_hospital.get_multi(db))
    recent_doctor_applications = await crud_doctor.get_doctors_by_status(db, status="pending", limit=5)
    total_revenue = await crud_transaction.get_total_revenue(db)
    revenue_chart_data = await crud_transaction.get_revenue_by_month(db)

    return {
        "stats": {
            "totalUsers": total_users,
            "totalDoctors": total_doctors,
            "pendingDoctorApprovals": pending_doctor_approvals,
            "totalHospitals": total_hospitals,
            "totalRevenue": total_revenue
        },
        "revenueChartData": revenue_chart_data,
        "recentDoctorApplications": recent_doctor_applications
    }

@router.get("/doctor-applications")
async def get_doctor_applications(status: Optional[str] = Query("pending", enum=["pending", "approved", "rejected"]),
                              db: AsyncSession = Depends(deps.get_db),
                              current_user=Depends(get_current_active_admin)):
    """
    Retrieves a list of doctor applications, with filtering capabilities.
    """
    applications = await crud_doctor.get_doctors_by_status(db, status=status)
    return {"applications": applications}

@router.patch("/doctor-applications/{app_id}")
async def update_doctor_application(
    app_id: int, 
    status_update: DoctorUpdate, 
    db: AsyncSession = Depends(deps.get_db), 
    current_user=Depends(get_current_active_admin)
):
    """
    Approves or rejects a specific doctor's application.
    """
    application = await crud_doctor.get(db, id=app_id)
    if not application:
        raise HTTPException(status_code=404, detail="Doctor application not found")
    
    updated_application = await crud_doctor.update(db, db_obj=application, obj_in=status_update)
    return updated_application

@router.get("/users")
async def get_users(search: Optional[str] = None, role: Optional[str] = None, page: int = 1, size: int = 10,
              db: AsyncSession = Depends(deps.get_db),
              current_user=Depends(get_current_active_admin)):
    """
    Retrieves a paginated list of all users, with filtering.
    """
    skip = (page - 1) * size
    if role:
        users = await crud_user.get_users_by_role(db, role=role, skip=skip, limit=size)
    else:
        users = await crud_user.get_all_users(db, email=search, skip=skip, limit=size)
    
    total_users = len(users)
    
    return {"total": total_users, "page": page, "size": size, "users": users}

@router.patch("/users/{user_id}")
async def update_user(user_id: int, updates: UserUpdate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Updates a user's status (block/unblock) or their token balance.
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await crud_user.update(db, db_obj=user, obj_in=updates)
    return updated_user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Permanently deletes a user from the platform.
    """
    try:
        await crud_user.remove(db, id=user_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/hospitals")
async def get_hospitals(db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Lists all hospitals.
    """
    hospitals = await crud_hospital.get_multi(db)
    return hospitals

@router.post("/hospitals")
async def create_hospital(hospital: HospitalCreate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Creates a new hospital.
    """
    return await crud_hospital.create(db, obj_in=hospital)

@router.put("/hospitals/{hospital_id}")
async def update_hospital(hospital_id: int, hospital: HospitalUpdate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Updates a hospital.
    """
    db_hospital = await crud_hospital.get(db, id=hospital_id)
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return await crud_hospital.update(db, db_obj=db_hospital, obj_in=hospital)

@router.delete("/hospitals/{hospital_id}")
async def delete_hospital(hospital_id: int, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
Deletes a hospital.
    """
    try:
        await crud_hospital.remove(db, id=hospital_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Hospital not found")

@router.post("/hospitals/import")
async def import_hospitals(file: UploadFile = File(...), db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Handles multipart/form-data upload of a CSV/Excel file to bulk-add hospitals.
    """
    contents = await file.read()
    file_like_object = io.BytesIO(contents)

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_like_object)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_like_object)
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV or Excel file.")

        hospitals_to_create = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            if 'departments' in row_dict:
                departments = row_dict['departments']
                if isinstance(departments, str):
                    # Keep it as a comma-separated string
                    pass
                elif isinstance(departments, list):
                    row_dict['departments'] = ",".join(departments)
            hospitals_to_create.append(HospitalCreate(**row_dict))

        for hospital in hospitals_to_create:
            await crud_hospital.create(db, obj_in=hospital)

        return {"status": "success", "imported_count": len(hospitals_to_create)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during file processing: {e}")


@router.get("/medications")
async def get_medications(search: Optional[str] = None, page: int = 1, size: int = 10,
                  db: AsyncSession = Depends(deps.get_db),
                  current_user=Depends(get_current_active_admin)):
    """
    Lists all medications with pagination and search.
    """
    skip = (page - 1) * size
    medications = await crud_medication.get_multi(db, skip=skip, limit=size)
    total_medications = len(medications)
    return {"total": total_medications, "page": page, "size": size, "medications": medications}

@router.post("/medications")
async def create_medication(medication: MedicationCreate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Creates a new medication entry.
    """
    return await crud_medication.create(db, obj_in=medication)

@router.put("/medications/{medication_id}")
async def update_medication(medication_id: int, medication: MedicationUpdate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Updates a medication entry.
    """
    db_medication = await crud_medication.get(db, id=medication_id)
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return await crud_medication.update(db, db_obj=db_medication, obj_in=medication)

@router.delete("/medications/{medication_id}")
async def delete_medication(medication_id: int, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Deletes a medication entry.
    """
    try:
        await crud_medication.remove(db, id=medication_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Medication not found")

@router.get("/medications/export-template")
async def export_medications_template(current_user=Depends(get_current_active_admin)):
    """
    Downloads a CSV file with only headers for bulk import.
    """
    output = io.StringIO()
    output.write("name,manufacturer,strength\n")
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=medication_template.csv"})

@router.post("/broadcast-notification")
async def broadcast_notification(notification: NotificationBroadcast, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Sends a notification to a targeted group of users.
    """
    users_to_notify = []
    if notification.target_audience == "ALL":
        users_to_notify = await crud_user.get_all_users(db)
    elif notification.target_audience == "ROLE" and notification.audience_role:
        users_to_notify = await crud_user.get_users_by_role(db, role=notification.audience_role)
    
    if not users_to_notify:
        raise HTTPException(status_code=404, detail="No users found for the specified audience.")

    for user in users_to_notify:
        notification_obj = NotificationCreate(message=notification.message, user_id=user.id)
        await crud_notification.create(db, obj_in=notification_obj)

    return Response(status_code=202, content={"status": "Notification sent successfully."})

@router.get("/income/stats")
async def get_income_stats(db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Provides an overview of total revenue, monthly earnings, and processing fees.
    """
    total_revenue = await crud_transaction.get_total_revenue(db)
    # Assuming processing fees are a fixed percentage or value
    processing_fees = total_revenue * 0.05  # Example: 5% processing fee
    monthly_earnings = await crud_transaction.get_revenue_by_month(db)

    return {
        "totalRevenue": total_revenue,
        "monthlyEarnings": monthly_earnings,
        "processingFees": processing_fees
    }

@router.get("/income/chart-data")
async def get_income_chart_data(db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Returns data formatted for graphical representation.
    """
    return await crud_transaction.get_revenue_by_month(db)

@router.get("/income/transactions")
async def get_income_transactions(page: int = 1, size: int = 10, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Lists all transactions with filtering and pagination.
    """
    skip = (page - 1) * size
    transactions = await crud_transaction.get_transactions(db, skip=skip, limit=size)
    total_transactions = len(await crud_transaction.get_multi(db))
    return {"total": total_transactions, "page": page, "size": size, "transactions": transactions}
