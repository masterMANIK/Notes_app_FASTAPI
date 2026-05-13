from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# 1. Create the SQLAlchemy "Engine"
# The engine is the core interface to the database.
engine = create_engine(settings.DATABASE_URL)

# 2. Create a SessionLocal class
# Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create a Base class
# We will use this class later to create our database models (like User and Note).
Base = declarative_base()

# 4. Create a Dependency to get the database session
# This will be used in our routes to safely open and close DB connections.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
