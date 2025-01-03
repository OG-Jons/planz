from fastapi import APIRouter

router = APIRouter(prefix="/plants", tags=["plants"])

@router.get("/")
def read_plants():
    return [{"name": "Golden Pothos"}, {"name": "Snake Plant"}]