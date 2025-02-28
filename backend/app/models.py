from datetime import datetime
from typing import List

from sqlmodel import SQLModel, Field, Relationship


class PlantBase(SQLModel):
    name: str
    species: str


class Plant(PlantBase, table=True):
    __tablename__ = "plant"
    id: int = Field(default=None, primary_key=True)
    stats: List["Stat"] = Relationship(back_populates="plant")

class PlantCreate(PlantBase):
    pass

class PlantPublic(PlantBase):
    id: int

class PlantPublicWithStats(PlantPublic):
    stats: List["Stat"]

class StatBase(SQLModel):
    humidity_score: float
    sunlight_score: float


class Stat(StatBase, table=True):
    __tablename__ = "stat"
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False)
    plant_id: int = Field(foreign_key="plant.id", ondelete="CASCADE")
    plant: Plant = Relationship(back_populates="stats")


class StatCreate(StatBase):
    pass
