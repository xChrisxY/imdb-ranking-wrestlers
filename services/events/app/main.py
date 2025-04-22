import uvicorn 
from fastapi import FastAPI, Depends ,HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx 
from sqlmodel import SQLModel, Session 

from app.api import events, shows
from app.core.config import settings 
from app.db.session import engine 

# Creamos las tablas en la base de datos
SQLModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="WWE Rankings Events Service",
    description="Servicio de gestión de eventos para la plataforma de rankings de WWE",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(shows.router, prefix="/shows", tags=["shows"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "events"}

    
@app.middleware("http")
async def verify_token(request, call_next):
    if request.url.path == "/health":
        response = await call_next(request)
        return response

    public_paths = [
        "/events",
        "/shows"
    ]
    
    # Verificamos si la ruta es pública y el método es GET
    path_is_public = any(request.url.path.startswith(p) for p in public_paths)
    if path_is_public and request.method == "GET":
        response = await call_next(request)
        return response

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Not authenticated"})

    # Verificamos el token con el servicio de autenticación
    try:

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.AUTH_SERVICE_URL}/users/me", headers={"Authorization": auth_header})

    except httpx.RequestError:
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"detail": "Auth service unavailable."})

    response = await call_next(request)
    return response
    


if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True)