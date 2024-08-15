from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

from typing import Generator

URL = settings.DATABASE_URL
engine = create_engine(URL)

sessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db() -> Generator:
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()