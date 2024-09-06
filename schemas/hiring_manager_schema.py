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
    job_id: Optional[int] = None
    title: str
    subtitle: Optional[str] = None
    description: str
    upload_date: datetime
    deadline: datetime
    stipend: float
    duration: str
    location: str
    technology_used: List[str]
    hiring_manager: Optional[int] = None
    approval: Optional[bool] = None
    jd_doc: Optional[str] = None
    perks: Optional[str] = None
    no_of_openings: int

    class Config:
        orm_mode = True

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
