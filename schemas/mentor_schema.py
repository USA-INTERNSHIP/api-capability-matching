from typing import Optional, List
from pydantic import BaseModel

class MentorProfileSchema(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    mobileNo: Optional[int] = None
