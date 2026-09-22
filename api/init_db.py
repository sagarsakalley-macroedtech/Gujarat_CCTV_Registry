from database import engine, Base

# Import models so SQLAlchemy knows about the tables
from models import Camera, Department, District


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")