from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

from typing import Generator

load_dotenv(".env")

URL = os.getenv("DATABASE_URL")
engine = create_engine(URL)

sessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db() -> Generator:
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()