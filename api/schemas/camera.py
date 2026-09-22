from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CameraCreate(BaseModel):
    camera_code: str
    department: Optional[str] = None
    district: Optional[str] = None
    camera_type: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = "active"


class CameraResponse(CameraCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True