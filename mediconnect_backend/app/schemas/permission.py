from pydantic import BaseModel
from typing import Dict, Any

class RolePermissionBase(BaseModel):
    role: str
    permissions: Dict[str, Any]

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermission(RolePermissionBase):
    id: int

    class Config:
        orm_mode = True
