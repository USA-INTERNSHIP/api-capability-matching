from sqlalchemy import Integer, String, Column, BigInteger, Boolean
from sqlalchemy.orm import relationship

from db.base_class import Base

class Users(Base):
    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password = Column(String)
    socialLogin = Column(Boolean, default=False)
    userRole = Column(String)

    # Relationship with HiringManager
    hiringManager = relationship('HiringManager', back_populates='user', uselist=False)

    # Relationship with Intern (new)
    internProfile = relationship('Intern', back_populates='user', uselist=False)
