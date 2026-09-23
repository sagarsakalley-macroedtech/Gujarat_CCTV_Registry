from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    department_code = Column(String(50), unique=True, nullable=False)
    department_name = Column(String(200), nullable=False)
    description = Column(Text)

    cameras = relationship("Camera", back_populates="department")


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    district_name = Column(String(100), unique=True, nullable=False)
    state = Column(String(100), default="Gujarat")

    cameras = relationship("Camera", back_populates="district")


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, autoincrement=True)

    camera_id = Column(String(50), unique=True, nullable=False)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    district_id = Column(
        Integer,
        ForeignKey("districts.id"),
        nullable=False
    )

    location_name = Column(String(250))
    taluka = Column(String(100))
    village = Column(String(150))

    latitude = Column(Float)
    longitude = Column(Float)

    camera_type = Column(String(100))
    manufacturer = Column(String(100))
    model = Column(String(100))

    ownership = Column(String(100))
    connectivity_type = Column(String(100))

    storage_type = Column(String(100))
    retention_days = Column(Integer)

    vms_vendor = Column(String(100))

    operational_status = Column(String(50))
    maintenance_status = Column(String(50))

    installation_date = Column(Date)

    amc_start_date = Column(Date)
    amc_end_date = Column(Date)

    description = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    department = relationship(
        "Department",
        back_populates="cameras"
    )

    district = relationship(
        "District",
        back_populates="cameras"
    )

    health_records = relationship(
        "CameraHealth",
        back_populates="camera",
        cascade="all, delete-orphan"
    )

    maintenance_records = relationship(
        "MaintenanceRecord",
        back_populates="camera",
        cascade="all, delete-orphan"
    )


class CameraHealth(Base):
    __tablename__ = "camera_health"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    camera_id = Column(
        Integer,
        ForeignKey("cameras.id"),
        nullable=False
    )

    is_online = Column(Boolean, default=True)

    last_seen = Column(DateTime)

    health_status = Column(String(50))

    remarks = Column(Text)

    camera = relationship(
        "Camera",
        back_populates="health_records"
    )


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    camera_id = Column(
        Integer,
        ForeignKey("cameras.id"),
        nullable=False
    )

    maintenance_date = Column(Date)

    issue_type = Column(String(200))

    action_taken = Column(Text)

    technician = Column(String(150))

    status = Column(String(50))

    camera = relationship(
        "Camera",
        back_populates="maintenance_records"
    )