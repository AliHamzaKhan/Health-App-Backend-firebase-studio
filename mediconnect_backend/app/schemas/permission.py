from pydantic import BaseModel
from typing import Dict, Any

class PermissionBase(BaseModel):
    role: str
    permissions: Dict[str, Any]

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class PermissionInDBBase(PermissionBase):
    id: int

    class Config:
        from_attributes = True

class Permission(PermissionInDBBase):
    pass
