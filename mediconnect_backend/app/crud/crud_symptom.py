


from app.crud.crud_base import CRUDBase
from app.schemas.symptom import SymptomCreate, SymptomUpdate
from app.models.symptom import Symptom

class CRUDSymptom(CRUDBase[Symptom, SymptomCreate, SymptomUpdate]):
    pass

symptom = CRUDSymptom(Symptom)
