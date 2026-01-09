from app.crud.base import CRUDBase
from app.models.medical_condition import MedicalCondition
from app.schemas.medical_condition import MedicalConditionCreate, MedicalCondition as MedicalConditionSchema

class CRUDMedicalCondition(CRUDBase[MedicalCondition, MedicalConditionCreate, MedicalConditionSchema]):
    pass

crud_medical_condition = CRUDMedicalCondition(MedicalCondition)
