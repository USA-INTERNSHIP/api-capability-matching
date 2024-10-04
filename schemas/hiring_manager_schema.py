from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# class IdDetails(BaseModel):
#     idProofName: Optional[str] = None
#     idProofNo: Optional[str] = None
#     idProofLink: Optional[str] = None
#
# class Company(BaseModel):
#     companyName: Optional[str] = None
#     companyAddress: Optional[str] = None

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

    # subtitle: Optional[str] = None
    # uploadDate: datetime  # Changed from upload_date to uploadDate
    # deadline: datetime
    # stipend: float
    # location: str
    # approval: Optional[bool] = None
    # jdDoc: Optional[str] = None
    # perks: Optional[str] = None
    # noOfOpenings: int

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
