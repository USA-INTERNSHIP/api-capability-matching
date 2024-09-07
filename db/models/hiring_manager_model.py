from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, BigInteger, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from db.base_class import Base
from sqlalchemy.types import TypeDecorator, TEXT
import json



class HiringManager(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mobileNo = Column(BigInteger)
    bio = Column(String)
    socialMedia = Column(String)
    idProofName = Column(String)
    idProofNo = Column(String)
    idProofLink = Column(String)
    companyName = Column(String)
    companyAddress = Column(String)
    roleApproval = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    user = relationship('Users', back_populates='hiringManager',uselist = False)
    # Relationships
    jobs = relationship('Job', back_populates='hiring_manager')

class Job(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    subtitle = Column(String)
    description = Column(String)
    upload_date = Column(DateTime, default=func.now())
    deadline = Column(DateTime)
    stipend = Column(Float)
    duration = Column(String)
    location = Column(String)
    technology_used = Column(String)  # Store as JSON string
    hiring_manager_id = Column(Integer, ForeignKey("hiringmanager.id"))
    hiring_manager = relationship("HiringManager", back_populates="jobs")
    approval = Column(Boolean, default=False)
    jd_doc = Column(String)
    perks = Column(String)
    no_of_openings = Column(Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'technology_used' in kwargs and isinstance(kwargs['technology_used'], list):
            self.technology_used = json.dumps(kwargs['technology_used'])

    @property
    def technology_used_list(self):
        return json.loads(self.technology_used) if self.technology_used else []

    @technology_used_list.setter
    def technology_used_list(self, value):
        if isinstance(value, list):
            self.technology_used = json.dumps(value)

    # Relationships for other entities like applications, contracts (for future use)
    # applications = relationship("Application", back_populates="job")
    # contracts = relationship("Contract", back_populates="job")

# Define other models similarly for Application, Review, Contract, etc.
