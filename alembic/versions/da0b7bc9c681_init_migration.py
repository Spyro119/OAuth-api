"""init_migration

Revision ID: da0b7bc9c681
Revises: 
Create Date: 2023-08-30 22:42:08.503853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'da0b7bc9c681'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password_changed', sa.VARCHAR(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.Column('password_expiration_delay', sa.INTEGER(), server_default=sa.text('30'), autoincrement=False, nullable=True),
    sa.Column('password_expired', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=True),
    sa.Column('date_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('date_updated', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('password_reset_link', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    # op.create_index('ix_permissions_id', 'permissions', ['id'], unique=False)
    op.create_table('token',
    sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('refresh_token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expires_in', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='token_user_id_fkey'),
    sa.PrimaryKeyConstraint('access_token', name='token_pkey')
    )
    # op.create_index('ix_token_access_token', 'token', ['access_token'], unique=False)
    op.create_table('groups',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='groups_pkey')
    )
    op.create_index('ix_groups_id', 'groups', ['id'], unique=False)
    op.create_table('user_groups',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='user_groups_group_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_groups_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_groups_pkey')
    )
    op.create_index('ix_user_groups_user_id', 'user_groups', ['user_id'], unique=False)
    op.create_table('permissions',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('permissions_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('group_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('version', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('obsolete', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('sync_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('obsolete_for_a_disabled_project', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='permissions_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('permission_groups',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('permission_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='permission_groups_group_id_fkey'),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], name='permission_groups_permission_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='permission_groups_pkey')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_groups_user_id', table_name='user_groups')
    op.drop_index('ix_groups_id', table_name='groups')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_index('ix_permissions_id', table_name='permissions')
    op.drop_index('ix_token_access_token', table_name='token')
    op.drop_table('permission_groups')
    op.drop_table('permissions')
    op.drop_table('user_groups')
    op.drop_table('groups')
    op.drop_table('token')
    op.drop_table('users')
    # ### end Alembic commands ###
