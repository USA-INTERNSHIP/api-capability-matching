from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base
import json

class Intern(Base):
    __tablename__ = 'intern'
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    mobileNo = Column(BigInteger, nullable=True)
    education = Column(String, nullable=True)

    # JSON fields
    skills = Column(String, nullable=True)  # Optional
    status = Column(String, nullable=True)  # Optional
    idDetails = Column(String, nullable=True)  # Optional
    company = Column(String, nullable=True)  # Optional

    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), unique=True)

    user = relationship('Users', back_populates='internProfile', uselist=False)
    applications = relationship("InternApplications", back_populates="intern")
    tasks = relationship("Tasks", back_populates="intern")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'skills' in kwargs and isinstance(kwargs['skills'], list):
            self.skills = json.dumps(kwargs['skills'])
        if 'idDetails' in kwargs and isinstance(kwargs['idDetails'], dict):
            self.idDetails = json.dumps(kwargs['idDetails'])
        if 'company' in kwargs and isinstance(kwargs['company'], dict):
            self.company = json.dumps(kwargs['company'])

    @property
    def skills_list(self):
        return json.loads(self.skills) if self.skills else []

    @skills_list.setter
    def skills_list(self, value):
        if isinstance(value, list):
            self.skills = json.dumps(value)

    @property
    def id_details_dict(self):
        return json.loads(self.idDetails) if self.idDetails else {}

    @id_details_dict.setter
    def id_details_dict(self, value):
        if isinstance(value, dict):
            self.idDetails = json.dumps(value)

    @property
    def company_dict(self):
        return json.loads(self.company) if self.company else {}

    @company_dict.setter
    def company_dict(self, value):
        if isinstance(value, dict):
            self.company = json.dumps(value)

    # Relationships for future entities like applications, contracts
    # applications = relationship("Application", back_populates="intern")
    # reviews = relationship("Review", back_populates="intern")
