from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from typing import Generator

# Load environment variables
load_dotenv(".env")

# Database URL from environment variables
URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(URL)   #,echo=True

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models to inherit from
Base = declarative_base()

# Dependency to get DB session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
