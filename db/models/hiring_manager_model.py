from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import relationship
from db.base_class import Base


class HiringManager(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mobileNo = Column(BigInteger)
    bio = Column(String)
    socialMedia = Column(String)
    idProofName = Column(String)
    idProofNo = Column(String)
    companyName = Column(String)
    companyAddress = Column(String)
    roleApproval = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    user = relationship('Users', back_populates='hiringManager',uselist = False)
    # Relationships
    # jobs = relationship("Job", back_populates="hiringManager")


class Job(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    salary = Column(Float)
    location = Column(String)
    # hiring_manager_id = Column(Integer, ForeignKey("hiringmanager.id"))
    #
    # hiring_manager = relationship("HiringManager", back_populates="jobs")

# Define other models similarly for Application, Review, Contract, etc.
