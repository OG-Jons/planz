from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
)

SessionLocal = sessionmaker(bind=engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session