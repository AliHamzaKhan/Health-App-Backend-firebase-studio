from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
import json

router = APIRouter()

@router.post("/seed_permissions/", status_code=201)
def seed_permissions(db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_active_superuser)):
    with open("app_user_view_permissions.json") as f:
        permissions_data = json.load(f)
    
    for role, permissions in permissions_data.items():
        permission_in = schemas.RolePermissionCreate(role=role, permissions=permissions)
        crud.permission.create(db=db, obj_in=permission_in)
    
    return {"message": "Permissions seeded successfully"}
