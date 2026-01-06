from app.crud.crud_base import CRUDBase
from app.db.base import Consultation
from app.schemas.consultation import ConsultationCreate, ConsultationUpdate
from sqlalchemy.ext.asyncio import AsyncSession

class CRUDConsultation(CRUDBase[Consultation, ConsultationCreate, ConsultationUpdate]):
    async def create_with_owner(self, db: AsyncSession, *, obj_in: ConsultationCreate, doctor_id: int) -> Consultation:
        db_obj = self.model(**obj_in.dict(), doctor_id=doctor_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

crud_consultation = CRUDConsultation(Consultation)
