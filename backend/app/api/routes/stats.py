import random, math

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utilities import repeat_every
from sqlmodel import Session, select, delete
from app.models import Stat, StatCreate, Plant
from app.core.db import get_session

router = APIRouter()

def calc_soil_percentage(soil_value: float, wet_moisture: float, dry_moisture: float) -> float:
    # TODO: If wet and dry is None, return raw soil_value, otherwise
    # calculate the percentage based on the provided values
    if wet_moisture is None or dry_moisture is None:
        return soil_value

    return round(100 - ((soil_value - wet_moisture) / (dry_moisture - wet_moisture)) * 100, 1)

@router.post("/plants/{plant_id}/stats", response_model=Stat)
def create_stat(
        plant_id: int,
        stat: StatCreate,
        session: Session = Depends(get_session)
):
    stat.sunlight_score = round(stat.sunlight_score, 1)
    plant = session.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db_stat = Stat(**stat.dict(), plant_id=plant_id)
    db_stat.soil_moisture_score = calc_soil_percentage(stat.soil_moisture_score, plant.soil_wet, plant.soil_dry)
    session.add(db_stat)
    session.commit()
    session.refresh(db_stat)
    return db_stat

@router.delete("/plants/{plant_id}/stats/reset")
def reset_stats(
        plant_id: int,
        session: Session = Depends(get_session)
):
    plant = session.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    statement = delete(Stat).where(Stat.plant_id == plant_id)
    session.exec(statement)
    session.commit()
    return {"message": "Stats reset successfully"}