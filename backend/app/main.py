from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel

from app.api.main import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    SQLModel.metadata.drop_all(engine)

app = FastAPI(
    title="Planz",
    lifespan=lifespan
)

sqlite_file_name = "plants.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app.include_router(api_router, prefix="/api")