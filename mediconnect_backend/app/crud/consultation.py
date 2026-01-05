from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.consultation import Consultation
from app.schemas.consultation import ConsultationCreate


class CRUDConsultation(CRUDBase[Consultation, ConsultationCreate, ConsultationCreate]):
    def create(self, db: Session, *, obj_in: ConsultationCreate, appointment_id: int) -> Consultation:
        db_obj = self.model(
            **obj_in.dict(), 
            appointment_id=appointment_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


consultation = CRUDConsultation(Consultation)
