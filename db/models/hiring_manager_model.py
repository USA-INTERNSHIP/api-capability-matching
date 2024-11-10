from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, BigInteger, DateTime, func
from sqlalchemy.orm import relationship
from db.base_class import Base
import json



class HiringManager(Base):
    __tablename__ = 'hiringmanager'
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    mobileNo = Column(BigInteger)

    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), unique=True)

    # Relationships
    user = relationship('Users', back_populates='hiring_manager',uselist = False)
    jobs = relationship('Job', back_populates='hiring_manager')
    mentor_applications = relationship("MentorApplications", back_populates="hiring_manager")

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    technologyUsed = Column(String)  # Store as JSON string
    scope = Column(String)
    description = Column(String)
    budget = Column(Float)
    duration = Column(String)

    hiring_manager_id = Column(Integer, ForeignKey("hiringmanager.id",ondelete="CASCADE"))
    mentor_id = Column(Integer, ForeignKey("mentor.id",ondelete="SET NULL"))

    mentor = relationship("Mentor", back_populates="jobs")
    hiring_manager = relationship("HiringManager", back_populates="jobs")

    mentor_applications = relationship("MentorApplications", back_populates="job")
    intern_applications = relationship("InternApplications", back_populates="job")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'technologyUsed' in kwargs and isinstance(kwargs['technologyUsed'], list):
            self.technologyUsed = json.dumps(kwargs['technologyUsed'])

    @property
    def technology_used_list(self):
        return json.loads(self.technologyUsed) if self.technologyUsed else []

    @technology_used_list.setter
    def technology_used_list(self, value):
        if isinstance(value, list):
            self.technologyUsed = json.dumps(value)

    # Relationships for other entities like applications, contracts (for future use)
    # applications = relationship("Application", back_populates="job")
    # contracts = relationship("Contract", back_populates="job")

# Define other models similarly for Application, Review, Contract, etc.
