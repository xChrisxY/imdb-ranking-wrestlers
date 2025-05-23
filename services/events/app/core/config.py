import os 
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "WWE Rankings Events Service"
    API_V1_STR: str = "/api/v1"
    DATABASE_URI: str = os.getenv("DATABASE_URI")
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")

    class Config:
        case_sensitive = True

settings = Settings()