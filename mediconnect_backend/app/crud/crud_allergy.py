from app.crud.base import CRUDBase
from app.models.allergy import Allergy
from app.schemas.allergy import AllergyCreate, Allergy as AllergySchema

class CRUDAllergy(CRUDBase[Allergy, AllergyCreate, AllergySchema]):
    pass

crud_allergy = CRUDAllergy(Allergy)
