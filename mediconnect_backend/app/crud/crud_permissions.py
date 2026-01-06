from app.crud.base import CRUDBase
from app.models.permission import RolePermission
from app.schemas.permission import RolePermissionCreate, RolePermission as RolePermissionSchema
from sqlalchemy.orm import Session

class CRUDPermission(CRUDBase[RolePermission, RolePermissionCreate, RolePermissionSchema]):
    def get_by_role(self, db: Session, *, role: str) -> RolePermission:
        return db.query(RolePermission).filter(RolePermission.role == role).first()

permission = CRUDPermission(RolePermission)
