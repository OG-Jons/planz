import random, math

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utilities import repeat_every
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from app.models import Stat, StatCreate, Plant
from app.core.db import get_session

router = APIRouter()

max_moisture = 520

def calc_soil_percentage(soil_value: float):
    # TODO: Verify true max-min values
    return 100 / max_moisture * soil_value

@router.post("/plants/{plant_id}/stats", response_model=Stat)
def create_stat(
        plant_id: int,
        stat: StatCreate,
        session: Session = Depends(get_session)
):
    stat.soil_moisture_score = calc_soil_percentage(stat.soil_moisture_score)
    plant = session.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_stat = Stat(**stat.dict(), plant_id=plant_id)
    session.add(db_stat)
    session.commit()
    session.refresh(db_stat)
    return db_stat