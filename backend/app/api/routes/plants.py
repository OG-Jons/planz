from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import Plant, PlantCreate, PlantPublicWithStats

router = APIRouter()

@router.get("/plants", response_model=List[PlantPublicWithStats])
def read_all_plants(
        minutes: Optional[int] = Query(None, ge=1, description="Filter stats from last N minutes"),
        session: Session = Depends(get_session)
):
    # Base query with relationship loading
    query = select(Plant).options(selectinload(Plant.stats))

    # Execute query to get all plants with their stats
    plants = session.exec(query).all()

    if minutes is not None:
        cutoff_time = datetime.now() - timedelta(minutes=minutes)

        # Filter stats for each plant
        for plant in plants:
            plant.stats = [stat for stat in plant.stats if stat.timestamp >= cutoff_time]

    return plants

@router.get("/plants/{plant_id}", response_model=PlantPublicWithStats)
def read_plant(
        plant_id: int,
        minutes: Optional[int] = Query(None, ge=1, description="Filter stats from last N minutes"),
        session: Session = Depends(get_session)):
    # Query with relationship loading
    query = (
        select(Plant)
            .where(Plant.id == plant_id)
            .options(selectinload(Plant.stats))
    )

    plant = session.exec(query).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    if minutes is not None:
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        plant.stats = [stat for stat in plant.stats if stat.timestamp >= cutoff_time]

    return plant

@router.post("/plants", response_model=Plant)
def create_plant(plant: PlantCreate, session: Session = Depends(get_session)):
    db_plant = Plant.model_validate(plant)
    session.add(db_plant)
    session.commit()
    session.refresh(db_plant)
    return db_plant