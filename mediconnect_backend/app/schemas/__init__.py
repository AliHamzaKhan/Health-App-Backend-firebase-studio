from .user import User, UserCreate, UserUpdate
from .patient import Patient, PatientCreate, PatientUpdate
from .doctor import Doctor, DoctorCreate, DoctorUpdate, DoctorDashboardStats
from .appointment import Appointment, AppointmentCreate, AppointmentUpdate
from .token import Token, TokenPayload
from .transaction import Transaction, TransactionCreate, TransactionUpdate
from .review import Review, ReviewCreate, ReviewUpdate
from .notification import Notification, NotificationCreate, NotificationUpdate
from .medication import Medication, MedicationCreate, MedicationUpdate
from .hospital import Hospital, HospitalCreate, HospitalUpdate
from .hospital_schedule import HospitalSchedule, HospitalScheduleCreate, HospitalScheduleUpdate
from .consultation import Consultation, ConsultationCreate, ConsultationUpdate
from .soap import SoapNote, SoapNoteCreate
from .subscription import Subscription, SubscriptionPurchase
from .permission import Permission,PermissionBase,PermissionCreate, PermissionUpdate,RolePermissionCreate
from .review import ReviewCreateForPatient, ReviewCreate
from .ai import Report, ReportSummary, SoapNoteGenerationResponse, AIModelBase, AIModelCreate, AIModel
from .ai_features import ReportAnalysisRequest, ReportAnalysisResponse, SymptomCheckerRequest, SymptomCheckerResponse, AllergyCheckerRequest, AllergyCheckerResponse, CalorieCheckerRequest, CalorieCheckerResponse
from .symptom import SymptomBase, SymptomCreate, SymptomUpdate, Symptom

Doctor.model_rebuild()
Appointment.model_rebuild()
Patient.model_rebuild()
