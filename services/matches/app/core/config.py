import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "WWE Rankings Matches Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URI: str = os.getenv("DATABASE_URI")
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL")
    WRESTLERS_SERVICE_URL: str = os.getenv("WRESTLERS_SERVICE_URL")
    EVENTS_SERVICE_URL: str = os.getenv("EVENTS_SERVICE_URL")

    class Config:
        case_sensitive = True

settings = Settings()


