import uvicorn 
from fastapi import FastAPI, Depends ,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx 
from sqlmodel import SQLModel, Session 

from app.api import events, shows
from app.core.config import settings 
from app.db.session import engine, Base, get_db 

SQLModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="WWE Rankings Events Service",
    description="Servicio de gestión de eventos para la plataforma de rankings de WWE",
    version="0.1.0"
)

if __name__ == '__main__':
    uvicorn.run("app:main.app", host="0.0.0.0", port=8003, reload=True)