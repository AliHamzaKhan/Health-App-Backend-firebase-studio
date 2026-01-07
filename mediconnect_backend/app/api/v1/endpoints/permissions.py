from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.api.v1 import deps
import json
from typing import Any, List, Optional

router = APIRouter()


@router.post("/seed_permissions/", status_code=201)
async def seed_permissions(db: AsyncSession = Depends(deps.get_db),
                           # current_user: models.User = Depends(deps.get_current_active_superuser)
                           ):
    with open("app_user_view_permissions.json") as f:
        permissions_data = json.load(f)

    for role, permissions in permissions_data.items():
        permission_in = schemas.RolePermissionCreate(role=role, permissions=permissions)
        await crud.permission.create(db=db, obj_in=permission_in)

    return {"message": "Permissions seeded successfully"}


@router.get("/", response_model=List[schemas.Permission])
async def read_permissions(
        db: AsyncSession = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        type: Optional[str] = Query(None, alias="type"),
        current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve permissions.
    """
    if type:
        permissions = await crud.permission.get_multi_by_type(
            db, type=type, skip=skip, limit=limit
        )
    else:
        permissions = await crud.permission.get_multi(db, skip=skip, limit=limit)
    return permissions


@router.post("/", response_model=schemas.Permission)
async def create_permission(
        *,
        db: AsyncSession = Depends(deps.get_db),
        permission_in: schemas.PermissionCreate,
        current_user: models.User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Create new permission.
    """
    permission = await crud.permission.create(db=db, obj_in=permission_in)
    return permission


@router.get("/{id}", response_model=schemas.Permission)
async def read_permission(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Get permission by ID.
    """
    permission = await crud.permission.get(db=db, id=id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.put("/{id}", response_model=schemas.Permission)
async def update_permission(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        permission_in: schemas.PermissionUpdate,
        current_user: models.User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Update permission.
    """
    permission = await crud.permission.get(db=db, id=id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    permission = await crud.permission.update(db=db, db_obj=permission, obj_in=permission_in)
    return permission
