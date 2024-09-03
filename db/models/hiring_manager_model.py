from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


class HiringManager(Base):
    __tablename__ = "hiring_managers"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationships
    jobs = relationship("Job", back_populates="hiring_manager")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    salary = Column(Float)
    location = Column(String)
    hiring_manager_id = Column(Integer, ForeignKey("hiring_managers.id"))

    hiring_manager = relationship("HiringManager", back_populates="jobs")

# Define other models similarly for Application, Review, Contract, etc.
