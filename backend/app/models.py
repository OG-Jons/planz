import datetime

from sqlmodel import SQLModel, Field, Relationship
import uuid

class PlantBase(SQLModel):
    name: str
    description: str

class PlantCreate(PlantBase):
    pass

class Plant(PlantBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    stats: list["PlantStat"] = Relationship(back_populates="plant", cascade_delete=True)


# -------------------------------- #
#            Statistics            #
# -------------------------------- #

# Stats Base, which includes a timestamp, an entry for soil moisture and light
class PlantStatBase(SQLModel):
    timestamp: datetime.datetime = datetime.datetime.now()
    soil_moisture: float
    light: float

class PlantStatsCreate(PlantStatBase):
    pass

class PlantStat(PlantStatBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    plant_id: uuid.UUID = Field(foreign_key="plant.id", nullable=False, ondelete="CASCADE")
    plant = Relationship(back_populates="stats")

class PlantStatPublic(PlantStatBase):
    id: uuid.UUID
    plant_id: uuid.UUID

class PlantStatsPublic(SQLModel):
    data: list[PlantStatPublic]
    count: int