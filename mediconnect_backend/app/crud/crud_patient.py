from typing import Optional
from app.crud.base import CRUDBase
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from sqlalchemy.orm import Session

class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Patient]:
        return db.query(Patient).filter(Patient.email == email).first()

patient = CRUDPatient(Patient)
