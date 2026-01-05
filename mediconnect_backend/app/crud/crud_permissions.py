import json
from typing import Dict, Any
from app.schemas.permissions import Permissions

class CRUDPermissions:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_default_permissions(self) -> Dict[str, Any]:
        default_permissions = {}
        for role, role_model_field in Permissions.model_fields.items():
            role_model = role_model_field.annotation
            default_permissions[role] = {}
            for feature in role_model.model_fields:
                default_permissions[role][feature] = True
        return default_permissions

    def get_permissions(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, "r") as f:
                content = f.read()
                if not content:
                    raise FileNotFoundError
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            default_perms = self.get_default_permissions()
            with open(self.file_path, "w") as f:
                json.dump(default_perms, f, indent=2)
            return default_perms

    def update_permissions(self, permissions: Permissions) -> Dict[str, Any]:
        permissions_data = permissions.model_dump()
        with open(self.file_path, "w") as f:
            json.dump(permissions_data, f, indent=2)
        return permissions_data

crud_permissions = CRUDPermissions("permissions.json")
