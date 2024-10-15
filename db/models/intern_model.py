from sqlalchemy import Column, Integer, ForeignKey, BigInteger, String
from sqlalchemy.orm import relationship
from db.base_class import Base

class Intern(Base):
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    mobileNo = Column(BigInteger)
    education = Column(String)  # You can add more fields as needed

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    user = relationship('Users', back_populates='internProfile', uselist=False)

    # Relationships for future entities like applications, contracts
    # applications = relationship("Application", back_populates="intern")
    # reviews = relationship("Review", back_populates="intern")
