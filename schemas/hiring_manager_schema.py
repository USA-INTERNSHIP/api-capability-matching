from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class IdDetails(BaseModel):
    idProofName: Optional[str] = None
    idProofNo: Optional[str] = None
    idProofLink: Optional[str] = None

class Company(BaseModel):
    companyName: Optional[str] = None
    companyAddress: Optional[str] = None

class HiringManagerProfileSchema(BaseModel):
    name: Optional[str] = None
    mobileNo: Optional[int] = None
    bio: Optional[str] = None  # Changed from int to str
    socialMedia: Optional[bool] = None
    roleApproval: Optional[bool] = None  # Added this field
    idDetails: Optional[IdDetails] = None
    company: Optional[Company] = None

class JobSchema(BaseModel):
    jobId: Optional[int] = None
    title: str
    subtitle: Optional[str] = None
    description: str
    uploadDate: datetime  # Changed from upload_date to uploadDate
    deadline: datetime
    stipend: float
    duration: str
    location: str
    technologyUsed: List[str]
    hiringManager: Optional[int] = None
    approval: Optional[bool] = None
    jdDoc: Optional[str] = None
    perks: Optional[str] = None
    noOfOpenings: int

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
