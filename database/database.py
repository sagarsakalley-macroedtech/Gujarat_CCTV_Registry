import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./cctv_registry.db"
)


# ============================================================
# SQLALCHEMY ENGINE
# ============================================================

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


# ============================================================
# BASE + SESSION
# ============================================================

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():
    """
    Create all database tables.
    """

    # Import models here to avoid circular imports
    from database import models

    Base.metadata.create_all(bind=engine)

    print("DATABASE INITIALIZED SUCCESSFULLY")


# ============================================================
# DATABASE SESSION
# ============================================================

def get_db():
    """
    Provides a database session.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()