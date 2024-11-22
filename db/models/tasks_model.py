from sqlalchemy import Integer, String, Column, ForeignKey, DATETIME
from sqlalchemy.orm import relationship

from db.base_class import Base


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    status = Column(String, nullable=True)
    description = Column(String, nullable=True)
    attachment = Column(String, nullable=True)
    assigned_date = Column(DATETIME, nullable=True)
    due_date = Column(DATETIME)
    completion_date = Column(DATETIME,nullable=True)
    feedback = Column(String, nullable=True)


    job_id = Column(Integer, ForeignKey('job.id',ondelete="CASCADE"))
    mentor_id = Column(Integer, ForeignKey('mentor.id',ondelete="CASCADE"))
    intern_id = Column(Integer, ForeignKey('intern.id',ondelete="CASCADE"))

    # Relationships
    job = relationship("Job", back_populates="tasks")
    mentor = relationship("Mentor", back_populates="tasks")
    intern = relationship("Intern", back_populates="tasks")
