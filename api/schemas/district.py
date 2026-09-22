from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DistrictCreate(BaseModel):
    name: str
    state: Optional[str] = "Gujarat"


class DistrictResponse(DistrictCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True