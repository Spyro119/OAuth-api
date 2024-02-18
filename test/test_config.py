from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import sys
import os

from test.utils.scaffold_db import authentication_token_for_admin, authentication_token_from_email
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py

from app.db.base_class import Base
from app.db.session import get_db
from app.api.v1.routes import router as v1_routes
from app.api.v1.adminRoutes import admin_router as v1_admin_routes
from app.db.config import test_settings

def start_application():
    app = FastAPI()
    app.include_router(v1_routes)
    app.include_router(v1_admin_routes)
    return app


SQLALCHEMY_DATABASE_URL = test_settings.TEST_DATABASE_URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(
    db_session: SessionTesting, app: FastAPI
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db_session: Session):
    return  authentication_token_from_email(
        client=client, email="testuser@hotmail.com", db=db_session
    )


@pytest.fixture(scope="module")
def admin_user_token_headers(client: TestClient, db_session: Session):
    return authentication_token_for_admin(
        client=client, email="admin_123@hotmail.com", db=db_session
    )