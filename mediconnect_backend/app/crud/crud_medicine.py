from app.crud.crud_base import CRUDBase
from app.schemas.medicine import MedicineCreate, MedicineUpdate
from app.db.base import Medicine

class CRUDMedicine(CRUDBase[Medicine, MedicineCreate, MedicineUpdate]):
    pass

crud_medicine = CRUDMedicine(Medicine)
