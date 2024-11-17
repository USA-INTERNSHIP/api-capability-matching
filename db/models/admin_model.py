from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Column, BigInteger, Boolean
from sqlalchemy.orm import relationship

from db.base_class import Base


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    socialLogin = Column(Boolean, default=False)
    userRole = Column(String, default="ADMIN")

    # Relationship to the Users table
    user = relationship("Users", back_populates="admin")
