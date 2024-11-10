from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class HiringManagerProfileSchema(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    mobileNo: Optional[int] = None


class JobSchema(BaseModel):
    jobId: Optional[int] = None

    title: str
    technologyUsed: List[str]
    scope: str
    description: str
    budget: float
    duration: str
    hiringManager: Optional[int] = None

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
