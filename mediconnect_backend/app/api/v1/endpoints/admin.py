from fastapi import APIRouter, Depends, Query, Response, UploadFile, File
from typing import Optional, List, Any
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
from app.schemas.response import StandardResponse

router = APIRouter()

@router.get("/dashboard-stats", response_model=StandardResponse[Any])
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

    data = {
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
    return StandardResponse(data=data, message="Dashboard stats retrieved successfully.")

@router.get("/doctor-applications", response_model=StandardResponse[Any])
async def get_doctor_applications(status: Optional[str] = Query("pending", enum=["pending", "approved", "rejected"]),
                              db: AsyncSession = Depends(deps.get_db),
                              current_user=Depends(get_current_active_admin)):
    """
    Retrieves a list of doctor applications, with filtering capabilities.
    """
    applications = await crud_doctor.get_doctors_by_status(db, status=status)
    return StandardResponse(data={"applications": applications}, message="Doctor applications retrieved successfully.")

@router.patch("/doctor-applications/{app_id}", response_model=StandardResponse[Doctor])
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
        return StandardResponse(success=False, message="Doctor application not found", data=None)
    
    updated_application = await crud_doctor.update(db, db_obj=application, obj_in=status_update)
    return StandardResponse(data=updated_application, message="Doctor application updated successfully.")

@router.get("/users", response_model=StandardResponse[Any])
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
    data = {"total": total_users, "page": page, "size": size, "users": users}
    return StandardResponse(data=data, message="Users retrieved successfully.")

@router.patch("/users/{user_id}", response_model=StandardResponse[User])
async def update_user(user_id: int, updates: UserUpdate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Updates a user's status (block/unblock) or their token balance.
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        return StandardResponse(success=False, message="User not found")
    updated_user = await crud_user.update(db, db_obj=user, obj_in=updates)
    return StandardResponse(data=updated_user, message="User updated successfully.")

@router.delete("/users/{user_id}", response_model=StandardResponse[Any])
async def delete_user(user_id: int, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Permanently deletes a user from the platform.
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        return StandardResponse(success=False, message="User not found")
    await crud_user.remove(db, id=user_id)
    return StandardResponse(message="User deleted successfully.")

@router.get("/hospitals", response_model=StandardResponse[List[Hospital]])
async def get_hospitals(db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Lists all hospitals.
    """
    hospitals = await crud_hospital.get_multi(db)
    return StandardResponse(data=hospitals, message="Hospitals retrieved successfully.")

@router.post("/hospitals", response_model=StandardResponse[Hospital])
async def create_hospital(hospital: HospitalCreate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Creates a new hospital.
    """
    new_hospital = await crud_hospital.create(db, obj_in=hospital)
    return StandardResponse(data=new_hospital, message="Hospital created successfully.")

@router.put("/hospitals/{hospital_id}", response_model=StandardResponse[Hospital])
async def update_hospital(hospital_id: int, hospital: HospitalUpdate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Updates a hospital.
    """
    db_hospital = await crud_hospital.get(db, id=hospital_id)
    if not db_hospital:
        return StandardResponse(success=False, message="Hospital not found")
    updated_hospital = await crud_hospital.update(db, db_obj=db_hospital, obj_in=hospital)
    return StandardResponse(data=updated_hospital, message="Hospital updated successfully.")

@router.delete("/hospitals/{hospital_id}", response_model=StandardResponse[Any])
async def delete_hospital(hospital_id: int, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Deletes a hospital.
    """
    hospital = await crud_hospital.get(db, id=hospital_id)
    if not hospital:
        return StandardResponse(success=False, message="Hospital not found")
    await crud_hospital.remove(db, id=hospital_id)
    return StandardResponse(message="Hospital deleted successfully.")

@router.post("/hospitals/import", response_model=StandardResponse[Any])
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
            return StandardResponse(success=False, message="Invalid file format. Please upload a CSV or Excel file.")

        hospitals_to_create = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            if 'departments' in row_dict:
                departments = row_dict['departments']
                if isinstance(departments, str):
                    pass
                elif isinstance(departments, list):
                    row_dict['departments'] = ",".join(departments)
            hospitals_to_create.append(HospitalCreate(**row_dict))

        for hospital in hospitals_to_create:
            await crud_hospital.create(db, obj_in=hospital)

        return StandardResponse(data={"imported_count": len(hospitals_to_create)}, message="Hospitals imported successfully.")

    except Exception as e:
        return StandardResponse(success=False, message=f"An error occurred during file processing: {e}")


@router.get("/medications", response_model=StandardResponse[Any])
async def get_medications(search: Optional[str] = None, page: int = 1, size: int = 10,
                  db: AsyncSession = Depends(deps.get_db),
                  current_user=Depends(get_current_active_admin)):
    """
    Lists all medications with pagination and search.
    """
    skip = (page - 1) * size
    medications = await crud_medication.get_multi(db, skip=skip, limit=size)
    total_medications = len(medications)
    data = {"total": total_medications, "page": page, "size": size, "medications": medications}
    return StandardResponse(data=data, message="Medications retrieved successfully.")

@router.post("/medications", response_model=StandardResponse[Medication])
async def create_medication(medication: MedicationCreate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Creates a new medication entry.
    """
    new_medication = await crud_medication.create(db, obj_in=medication)
    return StandardResponse(data=new_medication, message="Medication created successfully.")

@router.put("/medications/{medication_id}", response_model=StandardResponse[Medication])
async def update_medication(medication_id: int, medication: MedicationUpdate, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Updates a medication entry.
    """
    db_medication = await crud_medication.get(db, id=medication_id)
    if not db_medication:
        return StandardResponse(success=False, message="Medication not found")
    updated_medication = await crud_medication.update(db, db_obj=db_medication, obj_in=medication)
    return StandardResponse(data=updated_medication, message="Medication updated successfully.")

@router.delete("/medications/{medication_id}", response_model=StandardResponse[Any])
async def delete_medication(medication_id: int, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Deletes a medication entry.
    """
    medication = await crud_medication.get(db, id=medication_id)
    if not medication:
        return StandardResponse(success=False, message="Medication not found")
    await crud_medication.remove(db, id=medication_id)
    return StandardResponse(message="Medication deleted successfully.")

@router.get("/medications/export-template")
async def export_medications_template(current_user=Depends(get_current_active_admin)):
    """
    Downloads a CSV file with only headers for bulk import.
    """
    output = io.StringIO()
    output.write("name,manufacturer,strength\n")
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=medication_template.csv"})

@router.post("/broadcast-notification", response_model=StandardResponse[Any])
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
        return StandardResponse(success=False, message="No users found for the specified audience.")

    for user in users_to_notify:
        notification_obj = NotificationCreate(message=notification.message, user_id=user.id)
        await crud_notification.create(db, obj_in=notification_obj)

    return StandardResponse(message="Notification sent successfully.")

@router.get("/income/stats", response_model=StandardResponse[Any])
async def get_income_stats(db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Provides an overview of total revenue, monthly earnings, and processing fees.
    """
    total_revenue = await crud_transaction.get_total_revenue(db)
    # Assuming processing fees are a fixed percentage or value
    processing_fees = total_revenue * 0.05  # Example: 5% processing fee
    monthly_earnings = await crud_transaction.get_revenue_by_month(db)

    data = {
        "totalRevenue": total_revenue,
        "monthlyEarnings": monthly_earnings,
        "processingFees": processing_fees
    }
    return StandardResponse(data=data, message="Income stats retrieved successfully.")

@router.get("/income/chart-data", response_model=StandardResponse[Any])
async def get_income_chart_data(db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Returns data formatted for graphical representation.
    """
    chart_data = await crud_transaction.get_revenue_by_month(db)
    return StandardResponse(data=chart_data, message="Income chart data retrieved successfully.")

@router.get("/income/transactions", response_model=StandardResponse[Any])
async def get_income_transactions(page: int = 1, size: int = 10, db: AsyncSession = Depends(deps.get_db), current_user=Depends(get_current_active_admin)):
    """
    Lists all transactions with filtering and pagination.
    """
    skip = (page - 1) * size
    transactions = await crud_transaction.get_transactions(db, skip=skip, limit=size)
    total_transactions = len(await crud_transaction.get_multi(db))
    data = {"total": total_transactions, "page": page, "size": size, "transactions": transactions}
    return StandardResponse(data=data, message="Income transactions retrieved successfully.")
