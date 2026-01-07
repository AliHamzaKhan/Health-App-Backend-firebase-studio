from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class PermissionBase(BaseModel):
    role: str
    permissions: Dict[str, Any]
    type: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RolePermissionCreate(PermissionBase):
    pass

class AdminPermissions(BaseModel):
    dashboard: bool
    doctorApplications: bool
    manageDoctors: bool
    manageHospitals: bool
    manageMedicines: bool
    manageUsers: bool
    notifications: bool
    income: bool
    permissions: bool

class DoctorPermissions(BaseModel):
    viewSchedule: bool
    patientRecords: bool
    createSoapNote: bool
    analyzeReport: bool
    messages: bool
    manageHospitals: bool
    incomeTracking: bool
    helpCenter: bool
    medicineDatabase: bool
    interactionChecker: bool
    subscription: bool
    profileAndSettings: bool

class PatientPermissions(BaseModel):
    addMedication: bool
    trackVitals: bool
    aiChatbot: bool
    analyzeReport: bool
    symptomChecker: bool
    allergyChecker: bool
    calorieChecker: bool
    findDoctors: bool
    nearbyHospitals: bool
    messages: bool
    manageTokens: bool
    helpCenter: bool
    viewAppointments: bool
    viewReports: bool
    viewMedications: bool
    profileAndSettings: bool

class Permissions(BaseModel):
    admin: AdminPermissions
    doctor: DoctorPermissions
    patient: PatientPermissions
