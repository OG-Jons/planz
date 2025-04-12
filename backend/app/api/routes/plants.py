import os
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.db import get_session
from app.models import Plant, PlantCreate, PlantPublicWithStats, PlantPublic
import filetype

router = APIRouter(prefix="/plants")

@router.get("", response_model=List[PlantPublicWithStats])
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

    # Sort plants after ID and then sort stats by timestamp
    plants = sorted(plants, key=lambda plant: plant.id)
    for plant in plants:
        plant.stats = sorted(plant.stats, key=lambda stat: stat.id)

    return plants

@router.get("/{plant_id}", response_model=PlantPublicWithStats)
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

    plant.stats = sorted(plant.stats, key=lambda stat: stat.id)

    return plant

@router.post("", response_model=Plant)
def create_plant(plant: PlantCreate, session: Session = Depends(get_session)):
    db_plant = Plant.model_validate(plant)
    session.add(db_plant)
    session.commit()
    session.refresh(db_plant)
    return db_plant

# Endpoint that accepts an image file, stores it in ./media and updates the plant's image field
@router.post("/{plant_id}/image", response_model=Plant)
def update_plant_image(plant_id: int, file: UploadFile, session: Session = Depends(get_session)):
    accepted_file_types = ["image/png", "image/jpeg", "image/jpg", "png", "jpeg", "jpg"]

    file_info = filetype.guess(file.file)
    if file_info is None:
        raise HTTPException(
            status_code=415,
            detail="Unable to determine file type",
        )

    file_extension = file_info.extension.lower()

    if file.content_type not in accepted_file_types or file_extension not in accepted_file_types:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type"
        )

    plant = session.get(Plant, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    # First delete the old file
    if plant.image and os.path.exists(f".{plant.image}"):
        os.remove(f".{plant.image}")

    image_path = f"./media/{plant_id}.{file_extension}"
    with open(image_path, "wb") as f:
        f.write(file.file.read())

    # Remove the dot from the beginning of the path
    image_path = image_path[1:]
    # Update plant's image field
    plant.image = image_path
    session.add(plant)
    session.commit()
    session.refresh(plant)
    return plant

@router.put("/{plant_id}", response_model=Plant)
def update_plant(plant_id: int, plant: PlantPublic, session: Session = Depends(get_session)):
    db_plant = session.get(Plant, plant_id)
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    db_plant.name = plant.name
    db_plant.species = plant.species
    db_plant.soil_wet = plant.soil_wet
    db_plant.soil_dry = plant.soil_dry

    session.add(db_plant)
    session.commit()
    session.refresh(db_plant)
    return db_plant

@router.delete("/{plant_id}", status_code=204)
def delete_plant(plant_id: int, session: Session = Depends(get_session)):
    db_plant = session.get(Plant, plant_id)
    if not db_plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    # First delete the old file
    if db_plant.image and os.path.exists(f".{db_plant.image}"):
        os.remove(f".{db_plant.image}")

    session.delete(db_plant)
    session.commit()
    return {"message": "Plant deleted successfully"}