from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, BigInteger, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from db.base_class import Base
from sqlalchemy.types import TypeDecorator, TEXT
import json



class HiringManager(Base):
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    mobileNo = Column(BigInteger)
    # bio = Column(String)
    # socialMedia = Column(String)
    # idProofName = Column(String)
    # idProofNo = Column(String)
    # idProofLink = Column(String)
    # companyName = Column(String)
    # companyAddress = Column(String)
    # roleApproval = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    user = relationship('Users', back_populates='hiringManager',uselist = False)
    # Relationships
    jobs = relationship('Job', back_populates='hiring_manager')

class Job(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    technologyUsed = Column(String)  # Store as JSON string
    scope = Column(String)
    description = Column(String)
    budget = Column(Float)
    duration = Column(String)

    # subtitle = Column(String)
    # upload_date = Column(DateTime, default=func.now())
    # deadline = Column(DateTime)
    # stipend = Column(Float)
    # location = Column(String)
    # approval = Column(Boolean, default=False)
    # jd_doc = Column(String)
    # perks = Column(String)
    # no_of_openings = Column(Integer)
    hiring_manager_id = Column(Integer, ForeignKey("hiringmanager.id"))
    hiring_manager = relationship("HiringManager", back_populates="jobs")

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
