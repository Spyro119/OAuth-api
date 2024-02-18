from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from app.db.config import settings
from app.db.session import engine
from app.db.base_class import Base

import app.api.v1.routes as v1_routes
import app.api.v1.adminRoutes as v1_Admin_routes

def create_tables():
	Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    
    return app

app = start_application()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_routes.router)
app.include_router(v1_Admin_routes.admin_router)
# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

@app.get("/", description="API pour authentifier les utilisateurs", status_code=301)
async def root():
    openapi_url = "/openapi.json"
    return get_swagger_ui_html(openapi_url=openapi_url, title="docs")

