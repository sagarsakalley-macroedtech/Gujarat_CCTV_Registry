from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./cctv_registry.db"
)


# =========================================================
# ENGINE
# =========================================================

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================================================
# BASE
# =========================================================

Base = declarative_base()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    # IMPORTANT:
    # Load all models before create_all()
    from . import models

    Base.metadata.create_all(
        bind=engine
    )


# =========================================================
# DATABASE SESSION
# =========================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()