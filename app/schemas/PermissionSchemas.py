from pydantic import BaseModel
from datetime import datetime


class PermissionGroup(BaseModel):
    id: int
    name: str
    is_active: bool


class PermissionSchema(BaseModel):
    id: int
    group_name: str
    code: str
    description: str
    version: str
    obsolete: bool = False
    sync_code: str
    obsolete_for_a_disabled_project: bool = False
    groups: list[PermissionGroup] | None

    class Config:
        from_attributes = True