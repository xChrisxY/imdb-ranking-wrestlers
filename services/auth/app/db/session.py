from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Creamos el motor de base de datos 
engine = create_engine(settings.DATABASE_URI, echo=True)

# Creamos las tablas automáticamente si no existen
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Generamos una sesión 
def get_db():
    with Session(engine) as session:
        yield session