from sqlmodel import create_engine, Session
from app.core.config import settings 

engine = create_engine(settings.DATABASE_URI)

def get_db():
    with Session(engine) as session:
        yield session
