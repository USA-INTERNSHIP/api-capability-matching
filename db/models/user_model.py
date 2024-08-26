from sqlalchemy import Integer, String, Column, BigInteger, Boolean
from db.base_class import Base

class Users(Base):
    id = Column(Integer,primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)
    email = Column(String,unique=True)
    password = Column(String)
    socialLogin = Column(Boolean, default=False)
    userRole = Column(String)

    firstName = Column(String)
    middleName = Column(String)
    lastName = Column(String)

    mobile = Column(BigInteger)
    gender = Column(String)
    highestQualification = Column(String)