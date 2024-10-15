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

class InternSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    mobileNo: Optional[str] = None
    skills: List[str]
    status: Optional[str] = None
    idDetails: Optional[IdDetails] = None
    company: Optional[Company] = None

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
