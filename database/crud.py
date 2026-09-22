from sqlalchemy.orm import Session

from database.models import (
    Department,
    District,
    Camera
)


# ---------------------------------------------------------
# DEPARTMENT
# ---------------------------------------------------------

def get_departments(db: Session):

    return db.query(
        Department
    ).order_by(
        Department.department_name
    ).all()


def get_department(
    db: Session,
    department_id: int
):

    return db.query(
        Department
    ).filter(
        Department.id == department_id
    ).first()


# ---------------------------------------------------------
# DISTRICT
# ---------------------------------------------------------

def get_districts(db: Session):

    return db.query(
        District
    ).order_by(
        District.district_name
    ).all()


# ---------------------------------------------------------
# CAMERAS
# ---------------------------------------------------------

def get_cameras(db: Session):

    return db.query(
        Camera
    ).order_by(
        Camera.camera_id
    ).all()


def get_camera(
    db: Session,
    camera_id: str
):

    return db.query(
        Camera
    ).filter(
        Camera.camera_id == camera_id
    ).first()


def create_camera(
    db: Session,
    camera_data: dict
):

    camera = Camera(
        **camera_data
    )

    db.add(camera)

    db.commit()

    db.refresh(camera)

    return camera


def delete_camera(
    db: Session,
    camera_id: str
):

    camera = get_camera(
        db,
        camera_id
    )

    if camera:

        db.delete(camera)

        db.commit()

        return True

    return False