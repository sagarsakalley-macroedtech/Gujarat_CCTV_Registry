from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base


DATABASE_URL = "sqlite:///cctv_registry.db"


engine = create_engine(
    DATABASE_URL,
    echo=False
)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def init_database():
    """
    Create all database tables.
    """

    Base.metadata.create_all(
        bind=engine
    )


def get_db():
    """
    Create database session.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()