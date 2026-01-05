from app.crud.crud_base import CRUDBase
from app.db.base import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate


class CRUDHospital(CRUDBase[Hospital, HospitalCreate, HospitalUpdate]):
    pass


hospital = CRUDHospital(Hospital)
