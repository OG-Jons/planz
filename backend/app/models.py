from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


class PlantBase(SQLModel):
    name: str
    species: str

class Plant(PlantBase, table=True):
    __tablename__ = "plant"
    id: int = Field(default=None, primary_key=True)
    image: str = Field(default=None, nullable=True)
    soil_wet: int = Field(default=None, nullable=True)
    soil_dry: int = Field(default=None, nullable=True)
    stats: List["Stat"] = Relationship(back_populates="plant")

class PlantCreate(PlantBase):
    pass

class PlantPublic(PlantBase):
    id: int
    image: Optional[str] = None
    soil_wet: Optional[int] = None
    soil_dry: Optional[int] = None

class PlantPublicWithStats(PlantPublic):
    stats: List["Stat"]

class StatBase(SQLModel):
    humidity_score: float
    sunlight_score: float
    temperature_score: float
    soil_moisture_score: float


class Stat(StatBase, table=True):
    __tablename__ = "stat"
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False)
    plant_id: int = Field(foreign_key="plant.id", ondelete="CASCADE")
    plant: Plant = Relationship(back_populates="stats")


class StatCreate(StatBase):
    pass
