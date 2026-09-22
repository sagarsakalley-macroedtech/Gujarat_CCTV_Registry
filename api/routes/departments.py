from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api.models import Department
from api.schemas.department import (
    DepartmentCreate,
    DepartmentResponse
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# GET ALL DEPARTMENTS
@router.get("/", response_model=List[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


# GET DEPARTMENT BY ID
@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# CREATE DEPARTMENT
@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Department).filter(
        Department.name == department.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    new_department = Department(
        **department.model_dump()
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


# UPDATE DEPARTMENT
@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department_data: DepartmentCreate,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    for key, value in department_data.model_dump().items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


# DELETE DEPARTMENT
@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }