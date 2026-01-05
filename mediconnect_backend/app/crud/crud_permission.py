from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    def get_by_role(self, db: Session, *, role: str) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.role == role).first()

    def get_all(self, db: Session) -> Dict[str, Any]:
        permissions = db.query(Permission).all()
        return {p.role: p.permissions for p in permissions}

crud_permission = CRUDPermission(Permission)
