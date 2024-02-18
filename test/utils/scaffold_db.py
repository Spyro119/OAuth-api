import json
from typing import Any, Generator
from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from app.models.Permission import Permission
from app.models.PermissionGroup import Permission_group
from app.utils.passwordUtils import create_refresh_token, get_hashed_password

from app.models.UserGroup import User_Group
from app.models.Group import Group
from app.models.User import User

def create_user(db_session: Session) -> User:
    password = get_hashed_password("VeryStrongPassword123!")

    db_user = User(
    username="unique_username",
    first_name = "Test",
    last_name = "User",
    email = "Test_user3@Testing.com",
    hashed_password = password,
    password_changed = True,
    password_expiration_delay = -1,
    password_expired = False,
    password_reset_link = None,
    is_active = True )
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

def create_reset_password_link(db_session: Session, db_user: User):
    db_user.password_reset_link = create_refresh_token(db_user.email, 60)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/api/v1/login/", data=data)
    response = r.json()
    auth_token = response["token"]["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def admin_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/api/v1/login/", data=data)
    response = r.json()
    auth_token = response["token"]["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    user = get_user_by_email(email=email, db=db)
    if not user:
        db_user =  User(
                        username="test_User2",
                        first_name = "Test",
                        last_name = "User",
                        email = email,
                        hashed_password = get_hashed_password(password),
                        password_changed = True,
                        password_expiration_delay = -1,
                        password_expired = False,
                        password_reset_link = None,
                        is_active = True )
        user = create_new_user(db_user=db_user, db_session=db)

        db_user2 = User(
            username = "uniq_username",
            email = "something@outlook.com",
            first_name = "test",
            last_name = "user",
            hashed_password = get_hashed_password("VeryStrongPassword123!"),
            password_expired = False,
            password_changed = False,
            password_expiration_delay = 30,
            is_active = True
        )
        user2 = create_new_user(db_user=db_user2, db_session=db)
    db_group = db.query(Group).filter(Group.name == "test-group").one_or_none()
    if db_group is None:
        db_group = Group(
            name= "test-group",
            description="testing group",
            is_active=True
        )
        group = create_new_group(db_group=db_group, db_session=db)
        if db_user.groups == []:
            add_user_to_group(db_user=db_user, db_group=db_group, db_session=db)
        else:
            for group in db_user.groups:
                if "test-group" not in group.name:
                    add_user_to_group(db_user=db_user, db_group=db_group, db_session=db)
    return user_authentication_headers(client=client, email=db_user.username, password=password)

def get_user_by_email(email:str,db:Session):
    db_user = db.query(User).filter(User.email == email).one_or_none()
    return db_user

def create_new_user(db_user: User, db_session: Session):
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user


def authentication_token_for_admin(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-admin-PassW0rd!"
    user = get_user_by_email(email=email, db=db)
    if not user:
        db_user =  User(
                        username="test_admin",
                        first_name = "Admin",
                        last_name = "User",
                        email = email,
                        hashed_password = get_hashed_password(password),
                        password_changed = True,
                        password_expiration_delay = -1,
                        password_expired = False,
                        password_reset_link = None,
                        is_active = True )
        user = create_new_user(db_user=db_user, db_session=db)

    group = db.query(Group).filter(Group.name == "admin").one_or_none()
    if not group:
        db_group = Group(
            name= "admin",
            description="Admin role",
            is_active=True
        )
        group = create_new_group(db_group=db_group, db_session=db)
    if db_user.groups == []:
        add_user_to_group(db_user=db_user, db_group=db_group, db_session=db)
    else:
        for group in db_user.groups:
            if "admin" not in group.name:
                add_user_to_group(db_user=db_user, db_group=db_group, db_session=db)
    return user_authentication_headers(client=client, email=db_user.username, password=password)


def create_new_group(db_group: Group, db_session: Session):
    db_session.add(db_group)
    db_session.commit()
    db_session.refresh(db_group)
    if db_group.name != "admin":
        db_permission = create_permission(db_group=db_group, db_session=db_session)
        create_permission_group(db_group=db_group, db_permission=db_permission, db_session=db_session)
    # create permissions
    return db_group

def create_permission(db_session: Session, db_group: Group = None):
    if db_group == None:
        group_name = "undefined"
    else:
        group_name = db_group.name
    db_permission = Permission(code="test",
                                    group_name= group_name, 
                                    description = "Test permission",
                                    version = "1.0.0",
                                    obsolete = False,
                                    sync_code = None,
                                    obsolete_for_a_disabled_project = False)
    db_session.add(db_permission)
    db_session.commit()
    db_session.refresh(db_permission)
    return db_permission

def create_permission_group(db_group: Group, db_permission: Permission, db_session: Session):
    db_permission_group = Permission_group(group_id=db_group.id, permission_id=db_permission.id)
    db_session.add(db_permission_group)
    db_session.commit()
    db_session.refresh(db_permission_group)

def add_user_to_group(db_user: User, db_group: Group, db_session: Session):
    db_user_group = User_Group(user_id=db_user.id, group_id=db_group.id)
    db_session.add(db_user_group)
    db_session.commit()
    db_session.refresh(db_user_group)