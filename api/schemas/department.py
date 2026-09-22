from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepartmentCreate(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None


class DepartmentResponse(DepartmentCreate):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True