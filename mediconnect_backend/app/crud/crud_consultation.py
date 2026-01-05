from app.crud.base import CRUDBase
from app.models.consultation import Consultation
from app.schemas.consultation import ConsultationCreate, ConsultationUpdate


class CRUDConsultation(CRUDBase[Consultation, ConsultationCreate, ConsultationUpdate]):
    pass


consultation = CRUDConsultation(Consultation)
