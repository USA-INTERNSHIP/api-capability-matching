from sqlalchemy import Integer, String, Column, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base


class MentorApplications(Base):
    __tablename__ = 'mentor_applications'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=True)
    job_id = Column(Integer, ForeignKey('job.id',ondelete="CASCADE"))
    mentor_id = Column(Integer, ForeignKey('mentor.id',ondelete="CASCADE"))
    hiring_manager_id = Column(Integer, ForeignKey('hiringmanager.id',ondelete="CASCADE"))

    # Relationships
    job = relationship("Job", back_populates="mentor_applications")
    mentor = relationship("Mentor", back_populates="mentor_applications")
    hiring_manager = relationship("HiringManager", back_populates="mentor_applications")


class InternApplications(Base):
    __tablename__ = 'intern_applications'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=True)
    job_id = Column(Integer, ForeignKey('job.id',ondelete="CASCADE"))
    intern_id = Column(Integer, ForeignKey('intern.id',ondelete="CASCADE"))
    mentor_id = Column(Integer, ForeignKey('mentor.id',ondelete="CASCADE"))

    # Relationships
    job = relationship("Job", back_populates="intern_applications")
    intern = relationship("Intern", back_populates="applications")
    mentor = relationship("Mentor", back_populates="intern_applications")