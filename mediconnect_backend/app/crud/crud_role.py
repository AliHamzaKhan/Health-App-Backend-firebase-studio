from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, Role as RoleSchema

class CRUDRole(CRUDBase[Role, RoleCreate, RoleSchema]):
    pass

crud_role = CRUDRole(Role)
