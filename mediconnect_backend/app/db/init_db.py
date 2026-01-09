import json
import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.db.base import Permission
import os
import json

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Get path to this script
    script_dir = os.path.dirname(__file__)
    # Construct path to JSON two levels up
    file_path = os.path.abspath(os.path.join(script_dir, "../../../app_user_view_permissions.json"))

    if not os.path.exists(file_path):
        logger.error(f"Permissions file not found: {file_path}")
        return

    with open(file_path, "r") as f:
        permissions_data = json.load(f)

    for role, permissions in permissions_data.items():
        permission_in = schemas.PermissionCreate(
            role=role,
            permissions=list(permissions.keys())
        )
        db_permission = crud.permission.get_by_role(db, role=role)

        if db_permission:
            crud.permission.update(db, db_obj=db_permission, obj_in=permission_in)
            logger.info(f"Permissions for role '{role}' updated.")
        else:
            crud.permission.create(db, obj_in=permission_in)
            logger.info(f"Permissions for role '{role}' created.")