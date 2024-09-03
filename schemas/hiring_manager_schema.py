from pydantic import BaseModel
from typing import Optional

class HiringManagerRegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class ProfileSchema(BaseModel):
    username: str
    bio: Optional[str]
    profile_image: Optional[str]

class JobSchema(BaseModel):
    title: str
    description: str
    salary: float
    location: str

class ApplicationSchema(BaseModel):
    job_id: int
    intern_id: int
    status: str

class ReviewSchema(BaseModel):
    intern_id: int
    rating: int
    feedback: Optional[str]

class ContractSchema(BaseModel):
    job_id: int
    intern_id: int
    terms: str
