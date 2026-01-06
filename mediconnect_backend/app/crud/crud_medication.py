from app.crud.crud_base import CRUDBase
from app.schemas.medication import MedicationCreate, MedicationUpdate
from app.db.base import Medication

class CRUDMedication(CRUDBase[Medication, MedicationCreate, MedicationUpdate]):
    pass

crud_medication = CRUDMedication(Medication)
