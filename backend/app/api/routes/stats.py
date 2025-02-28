from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models import Stat, StatCreate, Plant
from app.core.db import get_session

router = APIRouter()

@router.post("/plants/{plant_id}/stats", response_model=Stat)
def create_stat(
        plant_id: int,
        stat: StatCreate,
        session: Session = Depends(get_session)
):
    plant = session.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_stat = Stat(**stat.dict(), plant_id=plant_id)
    session.add(db_stat)
    session.commit()
    session.refresh(db_stat)
    return db_stat