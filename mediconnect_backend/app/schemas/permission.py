from pydantic import BaseModel
from typing import Dict, Any

class PermissionBase(BaseModel):
    role: str
    permissions: Dict[str, Any]

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True
