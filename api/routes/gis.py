from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Camera

router = APIRouter(
    prefix="/gis",
    tags=["GIS"]
)


@router.get("/cameras")
def get_camera_locations(
    db: Session = Depends(get_db)
):
    cameras = (
        db.query(Camera)
        .filter(
            Camera.latitude.isnot(None),
            Camera.longitude.isnot(None)
        )
        .all()
    )

    return {
        "total": len(cameras),
        "cameras": [
            {
                "id": camera.id,
                "camera_code": camera.camera_code,
                "department": camera.department,
                "district": camera.district,
                "camera_type": camera.camera_type,
                "location": camera.location,
                "latitude": camera.latitude,
                "longitude": camera.longitude,
                "status": camera.status
            }
            for camera in cameras
        ]
    }