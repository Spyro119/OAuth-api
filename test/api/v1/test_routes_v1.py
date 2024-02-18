from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from test.test_config import client, get_db, app, db_session, normal_user_token_headers
from test.utils.scaffold_db import create_reset_password_link, create_user, get_user_by_email
from sqlalchemy.orm import Session
from app.utils.passwordUtils import create_refresh_token, get_hashed_password
from app.models.User import User
from fastapi import status


api_version = "/api/v1"

def test_reset_password(client: TestClient, db_session: Session):
    """
    Teste qu'un nouvel utilistateur puisses changer son mot de passes.
    """
    data = { "password":"VeryStrongPasswordpart2!", 
             "confirm_password": "VeryStrongPasswordpart2!",
             "password_expiration_delay": 30 }
    user_created = create_user(db_session)
    email_res = client.patch(f"{api_version}/forgot-password?user_login={user_created.username}")
    reset_password_url = f"{api_version}/reset-password/{user_created.password_reset_link}"
    password_reset_link_status = client.get(reset_password_url)
    change_password = client.patch(reset_password_url, json=data)
    
    assert email_res.status_code ==  202
    assert email_res.json() == {"message": "An email has been sent."}
    assert password_reset_link_status.status_code == 204
    assert change_password.status_code == 202


def test_login_logout(client: TestClient, db_session: Session):
    user_created = get_user_by_email("Test_user3@Testing.com", db_session)
    login_response = client.post(f"{api_version}/login", data={
        "username": user_created.username, 
        "password": "VeryStrongPasswordpart2!"})
    response = login_response.json()
    access_token = response["token"]["access_token"]

    logout_response = client.post(f"{api_version}/logout", headers = {"Authorization": f"Bearer {access_token}"})
    
    assert login_response.status_code == 200
    assert response["token"]["access_token"] != None
    assert response["token"]["refresh_token"] != None
    assert response["token"]["expire"] != None
    assert logout_response.status_code == 204


def test_get_current_user_has_permission(client: TestClient, db_session: Session, normal_user_token_headers):
    has_not_permission_response = client.get(f"{api_version}/current-user-has-permission/admin", headers=normal_user_token_headers)
    has_permission_response = client.get(f"{api_version}/current-user-has-permission/test", headers=normal_user_token_headers)
    assert has_not_permission_response.status_code == 403
    assert has_permission_response.status_code == 200
    assert has_permission_response.json()["has_permission"] == True


def test_get_profile(client: TestClient, db_session: Session, normal_user_token_headers):
    profile_response = client.get(f"{api_version}/profile/", headers=normal_user_token_headers)
    
    assert profile_response.status_code == 200
    assert profile_response.json()["username"] == "test_User2"


def test_refresh_token(client, db_session):
    user_created = get_user_by_email("Test_user3@Testing.com", db_session)
    login_response = client.post(f"{api_version}/login", data={
        "username": user_created.username, 
        "password": "VeryStrongPasswordpart2!"})
    response = login_response.json()
    access_token = response["token"]["access_token"]
    refresh_token = response["token"]["refresh_token"]
    refresh_token_response = client.post(f"{api_version}/refresh-token?token={refresh_token}", headers = {"Authorization": f"Bearer {access_token}"})
    
    assert refresh_token_response.status_code == 201
    assert refresh_token_response.json()["token"]["access_token"] != None
    assert refresh_token_response.json()["token"]["refresh_token"] != None
    assert refresh_token_response.json()["token"]["expire"] != None
    return