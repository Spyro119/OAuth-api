import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Test_Settings:
    PROJECT_NAME:str = "Segidoc OAuth"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.getenv("TEST_POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("TEST_POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("TEST_POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("TEST_POSTGRES_DB")
    TEST_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

test_settings = Test_Settings()

class Settings:
    PROJECT_NAME:str = "Segidoc OAuth"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()
