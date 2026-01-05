import json
import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.models.permission import Permission

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    with open("app_user_view_permissions.json", "r") as f:
        permissions_data = json.load(f)

    for role, permissions in permissions_data.items():
        permission_in = schemas.PermissionCreate(role=role, permissions=permissions)
        db_permission = crud.crud_permission.get_by_role(db, role=role)

        if db_permission:
            crud.crud_permission.update(db, db_obj=db_permission, obj_in=permission_in)
            logger.info(f"Permissions for role '{role}' updated.")
        else:
            crud.crud_permission.create(db, obj_in=permission_in)
            logger.info(f"Permissions for role '{role}' created.")
