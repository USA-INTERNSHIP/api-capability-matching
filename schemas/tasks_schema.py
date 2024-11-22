from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class TaskSchema(BaseModel):
   title: str
   status: Optional[str] = "Pending"
   description: Optional[str] = None
   attachment: Optional[str] = None
   assigned_date: Optional[datetime] = datetime.now()
   due_date: datetime
   completion_date: Optional[datetime] = None
   feedback: Optional[str] = None

   job_id: Optional[int]
   intern_id: Optional[int]

   @field_validator('due_date')
   def validate_due_date(cls, due_date, info):
       assigned_date = info.data.get('assigned_date', datetime.now())  # Get assigned_date or current time
       if due_date < assigned_date:
           raise ValueError("Due date must be after assigned date")
       return due_date

   # @field_validator('completed_date')
   # def validate_completed_date(cls, completed_date, info):
   #     if completed_date:
   #         assigned_date = info.data.get('assigned_date', datetime.now())
   #         if completed_date < assigned_date:
   #             raise ValueError("Completion date must be after assigned date")
   #         if 'due_date' in info.data and info.data['due_date']:
   #             if completed_date > info.data['due_date']:
   #                 raise ValueError("Completion date cannot be after due date")
   #     return completed_date