from app.crud.crud_base import CRUDBase
from app.schemas.vital import VitalCreate, VitalUpdate
from app.models.vital import Vital

class CRUDVital(CRUDBase[Vital, VitalCreate, VitalUpdate]):
    pass

vital = CRUDVital(Vital)
