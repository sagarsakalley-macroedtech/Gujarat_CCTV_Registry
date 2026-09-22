from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.models import Camera
from api.schemas.camera import CameraCreate, CameraResponse

router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"]
)


# GET ALL CAMERAS
@router.get("/", response_model=List[CameraResponse])
def get_cameras(db: Session = Depends(get_db)):
    return db.query(Camera).all()


# GET CAMERA BY ID
@router.get("/{camera_id}", response_model=CameraResponse)
def get_camera(
    camera_id: int,
    db: Session = Depends(get_db)
):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    return camera


# CREATE CAMERA
@router.post("/", response_model=CameraResponse)
def create_camera(
    camera: CameraCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Camera).filter(
        Camera.camera_code == camera.camera_code
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Camera code already exists"
        )

    new_camera = Camera(
        **camera.model_dump()
    )

    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)

    return new_camera


# UPDATE CAMERA
@router.put("/{camera_id}", response_model=CameraResponse)
def update_camera(
    camera_id: int,
    camera_data: CameraCreate,
    db: Session = Depends(get_db)
):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    for key, value in camera_data.model_dump().items():
        setattr(camera, key, value)

    db.commit()
    db.refresh(camera)

    return camera


# DELETE CAMERA
@router.delete("/{camera_id}")
def delete_camera(
    camera_id: int,
    db: Session = Depends(get_db)
):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    db.delete(camera)
    db.commit()

    return {
        "message": "Camera deleted successfully"
    }