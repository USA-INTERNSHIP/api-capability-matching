from sqlalchemy import Integer, String, Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Mentor(Base):
    __tablename__ = 'mentor'
    id = Column(Integer, primary_key=True, index=True)

    firstName = Column(String)
    lastName = Column(String)
    mobileNo = Column(BigInteger)

    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"),unique=True)

    jobs = relationship("Job", back_populates="mentor")
    user = relationship("Users", back_populates="mentor", uselist = False)

    mentor_applications = relationship("MentorApplications", back_populates="mentor")
    intern_applications = relationship("InternApplications", back_populates="mentor")
    tasks = relationship("Tasks", back_populates="mentor")
