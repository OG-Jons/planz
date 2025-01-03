from fastapi import APIRouter

from app.api.routes import plants

api_router = APIRouter()

api_router.include_router(plants.router)