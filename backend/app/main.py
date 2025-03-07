from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.db import engine, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield
    # Clean up on shutdown
    engine.dispose()

# Create the FastAPI app with name "planz"
app = FastAPI(
    title="planz",
    description="A plant care tracker",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")
app.mount("/api/media", StaticFiles(directory="media"), name="media")