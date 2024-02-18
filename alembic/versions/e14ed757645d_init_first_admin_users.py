"""init first admin users

Revision ID: e14ed757645d
Revises: da0b7bc9c681
Create Date: 2023-08-30 23:04:01.704809

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, TIMESTAMP, Boolean

from app.utils.passwordUtils import get_hashed_password



# revision identifiers, used by Alembic.
revision: str = 'e14ed757645d'
down_revision: Union[str, None] = 'da0b7bc9c681'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    group_table = table(
        "groups",
        column("id", Integer),
        column("name", String),
        column("description", String),
        column("is_active", sa.Boolean())
    )
    user_table = table(
        "users",
        column("id",Integer),
        column("username",String),
        column("first_name",String),
        column("last_name",String),
        column("email", String),
        column("hashed_password", String),
        column("password_changed", String),
        column("password_expiration_delay", Integer),
        column("password_reset_link", String),
        column("password_expired", sa.Boolean()),
        column("is_active",sa.Boolean()),
        column("date_created", TIMESTAMP),
        column("date_updated", TIMESTAMP)
    )
    user_group_table = table(
        "user_groups",
        column("id", Integer),
        column("group_id", Integer),
        column("user_id", Integer)
    )
    op.bulk_insert(
        user_table, 
        [
            {
                "id": 1,
                "username": "admin",
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@hotmail.com",
                "hashed_password": get_hashed_password("password123!"),
                "is_active": True,
                "password_expired": True,
                "password_changed": "True",
                "password_expiration_delay": -1,
                "password_reset_link": "reset-password",
                "date_created": datetime.now(),
                "date_updated": None
            }
        ]
    )
    
    op.bulk_insert(
        group_table,
        [
            {
                "id": 1,
                "name": "Admin",
                "description": "Admin role",
                "is_active": True,
            }
        ]
    )
    op.bulk_insert(
        user_group_table,
        [
            {
                "id": 1,
                "group_id": 1,
                "user_id": 1
            }
        ]
    )
    pass


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE id = 1; \
                DELETE FROM groups WHERE name = 'admin'; \
                DELETE FROM user_groups WHERE id = 1;")
    pass
