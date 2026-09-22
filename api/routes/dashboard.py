from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Camera, Department, District

router = APIRouter()


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):

    total_cameras = db.query(Camera).count()

    active_cameras = (
        db.query(Camera)
        .filter(Camera.status == "active")
        .count()
    )

    inactive_cameras = (
        db.query(Camera)
        .filter(Camera.status != "active")
        .count()
    )

    total_departments = db.query(Department).count()

    total_districts = db.query(District).count()

    # Calculate active percentage
    if total_cameras > 0:
        active_percentage = round(
            (active_cameras / total_cameras) * 100,
            2
        )
    else:
        active_percentage = 0

    return {
        "total_cameras": total_cameras,
        "active_cameras": active_cameras,
        "inactive_cameras": inactive_cameras,
        "active_percentage": active_percentage,
        "total_departments": total_departments,
        "total_districts": total_districts
    }