from pydantic import BaseModel
from app.schemas.PermissionSchemas import PermissionSchema


class GroupUsers(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

class GroupSchema(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool = 1
    permissions: list[PermissionSchema] | None
    users: list[GroupUsers] | None
    class Config:
        from_attributes = True


class CreateGroupSchema(BaseModel):
    name: str
    description: str
    is_active: bool = 1

class AdminCreateGroupSchema(CreateGroupSchema):
    user_ids: list[int] | None = None
    permission_ids: list[int] | None = None
