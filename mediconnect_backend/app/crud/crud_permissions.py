from app.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, Permission as PermissionSchema
from sqlalchemy.orm import Session

class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionSchema]):
    def get_by_role(self, db: Session, *, role: str) -> Permission:
        return db.query(Permission).filter(Permission.role == role).first()

permission = CRUDPermission(Permission)
