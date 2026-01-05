from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
def get_all_permissions(
    db: Session = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve all permissions for all roles.
    """
    return crud.crud_permission.get_all(db)

@router.post("/")
def set_permissions(
    *,
    db: Session = Depends(deps.get_db),
    permission_in: PermissionCreate,
    # current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Create or update permissions for a specific role.
    """
    db_permission = crud.crud_permission.get_by_role(db, role=permission_in.role)
    if db_permission:
        return crud.crud_permission.update(db, db_obj=db_permission, obj_in=permission_in)
    return crud.crud_permission.create(db, obj_in=permission_in)


@router.get("/{role}")
def get_permissions_by_role(
    role: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve permissions for a specific role.
    """
    permission = crud.crud_permission.get_by_role(db, role=role)
    if not permission:
        raise HTTPException(status_code=404, detail="Role not found")
    return permission.permissions
