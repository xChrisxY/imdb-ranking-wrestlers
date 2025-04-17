import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from app.api import auth, users
from app.core.config import settings
from app.db.session import get_db, engine

# Creamos las tablas en la base de datos automáticamente
SQLModel.metadata.create_all(bind=engine)

app = FastAPI(title="WWE Rankings Auth Service", description="Servicio de autenticación para la plataforma de rankings de WWE", version="0.1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Endpoint de prueba de salud
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "auth"}

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)