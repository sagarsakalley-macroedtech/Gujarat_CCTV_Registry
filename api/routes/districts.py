from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.models import District
from api.schemas.district import (
    DistrictCreate,
    DistrictResponse
)

router = APIRouter(
    prefix="/districts",
    tags=["Districts"]
)


# GET ALL DISTRICTS
@router.get("/", response_model=List[DistrictResponse])
def get_districts(db: Session = Depends(get_db)):
    return db.query(District).all()


# GET DISTRICT BY ID
@router.get("/{district_id}", response_model=DistrictResponse)
def get_district(
    district_id: int,
    db: Session = Depends(get_db)
):
    district = db.query(District).filter(
        District.id == district_id
    ).first()

    if not district:
        raise HTTPException(
            status_code=404,
            detail="District not found"
        )

    return district


# CREATE DISTRICT
@router.post("/", response_model=DistrictResponse)
def create_district(
    district: DistrictCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(District).filter(
        District.name == district.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="District already exists"
        )

    new_district = District(
        **district.model_dump()
    )

    db.add(new_district)
    db.commit()
    db.refresh(new_district)

    return new_district


# UPDATE DISTRICT
@router.put("/{district_id}", response_model=DistrictResponse)
def update_district(
    district_id: int,
    district_data: DistrictCreate,
    db: Session = Depends(get_db)
):
    district = db.query(District).filter(
        District.id == district_id
    ).first()

    if not district:
        raise HTTPException(
            status_code=404,
            detail="District not found"
        )

    for key, value in district_data.model_dump().items():
        setattr(district, key, value)

    db.commit()
    db.refresh(district)

    return district


# DELETE DISTRICT
@router.delete("/{district_id}")
def delete_district(
    district_id: int,
    db: Session = Depends(get_db)
):
    district = db.query(District).filter(
        District.id == district_id
    ).first()

    if not district:
        raise HTTPException(
            status_code=404,
            detail="District not found"
        )

    db.delete(district)
    db.commit()

    return {
        "message": "District deleted successfully"
    }