from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
