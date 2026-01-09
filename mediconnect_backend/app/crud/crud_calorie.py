from app.crud.base import CRUDBase
from app.models.calorie import Calorie
from app.schemas.calorie import CalorieCreate, CalorieUpdate


class CRUDCalorie(CRUDBase[Calorie, CalorieCreate, CalorieUpdate]):
    pass


crud_calorie = CRUDCalorie(Calorie)
