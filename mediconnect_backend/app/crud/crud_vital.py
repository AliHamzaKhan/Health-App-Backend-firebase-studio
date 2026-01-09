from app.crud.base import CRUDBase
from app.models.vital import Vital
from app.schemas.vital import VitalCreate, VitalUpdate

vital = CRUDBase[Vital, VitalCreate, VitalUpdate](Vital)
