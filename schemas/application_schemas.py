from typing import Optional

from pydantic import BaseModel, Field


class ApplicationMentorSchema(BaseModel):
    status: Optional[str] = None
    jobId: Optional[int] = None
    mentorId: Optional[int] = None

class MentorModifyApplications(BaseModel):
    applicationId: Optional[int] = None
    status: Optional[str] = None
    jobId: Optional[int] = None
    mentorId: Optional[int] = None

class ApplicationInternSchema(BaseModel):
    status: Optional[str] = None
    jobId: Optional[int] = None
    internId: Optional[int] = None