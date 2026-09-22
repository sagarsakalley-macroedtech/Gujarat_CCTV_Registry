from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from api.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    camera_code = Column(String(100), unique=True, nullable=False, index=True)

    department = Column(String(150), nullable=True)
    district = Column(String(150), nullable=True)

    camera_type = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    status = Column(String(50), default="active")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=True)

    description = Column(String(500), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    state = Column(String(100), default="Gujarat")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )