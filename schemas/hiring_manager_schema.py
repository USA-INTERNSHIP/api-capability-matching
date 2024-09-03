from dataclasses import Field

from pydantic import BaseModel
from typing import Optional

class HiringManagerProfileSchema(BaseModel):
    name: str
    mobileNo: int
    bio: int
    socialMedia: bool
    idProofName: str
    idProofNo: str
    companyName: str
    companyAddress: str

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
