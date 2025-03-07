from fastapi import APIRouter
from starlette.staticfiles import StaticFiles

from app.api.routes import plants, stats

api_router = APIRouter()

api_router.include_router(plants.router)
api_router.include_router(stats.router)