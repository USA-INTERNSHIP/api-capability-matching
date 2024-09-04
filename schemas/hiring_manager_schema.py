
from typing import Optional
from pydantic import BaseModel

class HiringManagerProfileSchema(BaseModel):
    name: Optional[str] = None
    mobileNo: Optional[int] = None
    bio: Optional[int] = None
    socialMedia: Optional[bool] = None
    idProofName: Optional[str] = None
    idProofNo: Optional[str] = None
    companyName: Optional[str] = None
    companyAddress: Optional[str] = None

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
