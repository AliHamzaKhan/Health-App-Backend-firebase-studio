from app.crud.base import CRUDBase
from app.models.allergy import Allergy
from app.schemas.allergy import AllergyCreate, AllergyUpdate

class CRUDAllergy(CRUDBase[Allergy, AllergyCreate, AllergyUpdate]):
    pass

crud_allergy = CRUDAllergy(Allergy)
