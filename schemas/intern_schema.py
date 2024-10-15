from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

# Schema for ID details related to an intern
class IdDetails(BaseModel):
    idProofName: Optional[str] = None  # Name of the ID proof
    idProofNo: Optional[str] = None  # ID proof number
    idProofLink: Optional[str] = None  # Link to the ID proof document (if available)

# Schema for Company details related to an intern's work experience
class Company(BaseModel):
    companyName: Optional[str] = None  # Name of the company
    companyAddress: Optional[str] = None  # Address of the company

# Schema for intern profile information
from pydantic import BaseModel
from typing import Optional, List

class InternProfileSchema(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    mobileNo: Optional[str] = None
    education: Optional[str] = None
    email: Optional[str] = None  # Add email field
    skills: Optional[List[str]] = None
    status: Optional[str] = None
    idDetails: Optional[Dict[str, str]] = None  # Dictionary for ID details
    company: Optional[Dict[str, str]] = None  # Dictionary for company details

# Schema for the job application submitted by the intern
class ApplicationSchema(BaseModel):
    job_id: int  # ID of the job being applied for
    intern_id: int  # ID of the intern applying
    status: str  # Application status (e.g., applied, rejected, accepted)

# Schema for reviews left by a hiring manager for the intern
class ReviewSchema(BaseModel):
    intern_id: int  # ID of the intern being reviewed
    rating: int  # Rating given to the intern
    feedback: Optional[str] = None  # Optional feedback text

# Schema for contracts between an intern and a company
class ContractSchema(BaseModel):
    job_id: int  # ID of the job associated with the contract
    intern_id: int  # ID of the intern involved
    terms: str  # Terms of the contract
