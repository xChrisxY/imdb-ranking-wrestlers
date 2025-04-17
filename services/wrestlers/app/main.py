import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
import httpx 
from sqlmodel import SQLModel, Session

from app.api import wrestlers
from app.core.config import settings 
from app.db.session import engine, get_db 

SQLModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="WWE Rankings Wrestlers Service", 
    description="Servicio de gestión de luchadores para la plataforma de rankings",
    version="0.1.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(wrestlers.router, prefix="/wrestlers", tags=["wrestlers"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "wrestlers"}

@app.middleware("http")
async def verify_token(request, call_next):
    pass