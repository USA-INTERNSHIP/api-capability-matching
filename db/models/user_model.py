from sqlalchemy import Integer, String, Column, BigInteger
from db.base_class import Base

class Users(Base):
    id = Column(Integer,primary_key=True, index=True)
    email = Column(String,unique=True)
    password = Column(String)
    firstName = Column(String)
    middleName = Column(String)
    lastName = Column(String)
    mobile = Column(BigInteger)
    gender = Column(String)
    highestQualification = Column(String)