from pydantic import BaseModel, Field
from typing import Optional

class EarthquakeRecord(BaseModel):
    place: str
    magnitude: float = Field(alias="mag")
    time_epoch: int = Field(alias="time")
    tsunami: int
    felt_reports: Optional[int] = Field(default=0, alias="felt")

    class Config:
        populate_by_name = True
