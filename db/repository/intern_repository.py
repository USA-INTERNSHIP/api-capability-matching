from fastapi import HTTPException
from sqlalchemy.orm import Session
import json

from db.models import Tasks
from db.models import InternApplications
from db.models.hiring_manager_model import Job, HiringManager
from db.models.intern_model import Intern  # Replace with the correct import for your intern model
from db.models.mentor_model import Mentor
from db.models.user_model import Users
from schemas.application_schemas import ApplicationInternSchema
from schemas.intern_schema import InternProfileSchema  # Replace with the correct import for your intern schema


# Function to convert Intern model instance to DTO format
def get_intern_dto(intern):

    return {
        "id": intern.id,
        "firstName": intern.firstName,
        "lastName": intern.lastName,
        "mobileNo": intern.mobileNo,
        "education": intern.education,
        "skills": intern.skills,
        "status": intern.status,
        "idDetails": intern.idDetails,
        "company": intern.company
    }


# Retrieve intern profile based on user_id
def retrieve_intern_profile(user_id: int, db: Session):
    profile = db.query(Intern).filter(Intern.user_id == user_id).first()
    if profile:
        # Deserialize JSON fields before returning the DTO
        profile.skills = json.loads(profile.skills) if profile.skills else []
        profile.idDetails = json.loads(profile.idDetails) if profile.idDetails else {}
        profile.company = json.loads(profile.company) if profile.company else {}
        user = db.query(Users).filter(Users.id == profile.user_id).first()
        profile = get_intern_dto(profile)
        profile.update({"email": user.email})
        return {"status": "success", "data": profile}
    else:
        raise HTTPException(status_code=404, detail="Intern not found")


# Update intern profile logic
def update_intern_profile(user_id: int, intern_data: InternProfileSchema, db: Session):
    try:
        # Ensure intern_data is validated and instantiated properly
        if not isinstance(intern_data, InternProfileSchema):
            raise HTTPException(status_code=400, detail="Invalid data format. Expected InternProfileSchema.")

        intern = db.query(Intern).filter(Intern.user_id == user_id).first()
        if not intern:
            raise HTTPException(status_code=404, detail="Intern not found")

        # Update the intern's profile fields
        intern.firstName = intern_data.firstName
        intern.lastName = intern_data.lastName
        intern.mobileNo = intern_data.mobileNo
        intern.education = intern_data.education
        intern.skills = json.dumps(intern_data.skills) if isinstance(intern_data.skills, list) else intern_data.skills
        intern.status = intern_data.status

        # Optionally update idDetails and company if present
        if intern_data.idDetails:
            intern.idDetails = json.dumps(intern_data.idDetails) if isinstance(intern_data.idDetails, dict) else intern_data.idDetails

        if intern_data.company:
            intern.company = json.dumps(intern_data.company) if isinstance(intern_data.company, dict) else intern_data.company

        # Commit the changes to the database
        db.commit()
        db.refresh(intern)

        # Deserialize JSON fields before returning
        intern.skills = json.loads(intern.skills) if intern.skills else []
        intern.idDetails = json.loads(intern.idDetails) if intern.idDetails else {}
        intern.company = json.loads(intern.company) if intern.company else {}

        return {"status": "success", "data": get_intern_dto(intern)}

    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

def view_available_jobs_logic(db: Session):
    try:
        # Query with explicit joins and column selection
        jobs = (
            db.query(
                # Job table columns
                Job.id,
                Job.title,
                Job.technologyUsed,
                Job.scope,
                Job.description,
                Job.duration,
                # HiringManager table columns
                HiringManager.firstName.label('hiring_manager_first_name'),
                HiringManager.lastName.label('hiring_manager_last_name'),
                # Mentor table columns
                Mentor.firstName.label('mentor_first_name'),
                Mentor.lastName.label('mentor_last_name')
            )
            # Join with HiringManager table
            .join(
                HiringManager,
                Job.hiring_manager_id == HiringManager.id
            )
            # Join with Mentor table
            .join(
                Mentor,
                Job.mentor_id == Mentor.id
            )
            .filter(Job.mentor_id.isnot(None))
            .all()
        )

        response_data = [
            {
                "id": job.id,
                "title": job.title,
                "technologyUsed": json.loads(job.technologyUsed),
                "scope": job.scope,
                "description": job.description,
                "duration": job.duration,
                "hiringManagerName": f"{job.hiring_manager_first_name} {job.hiring_manager_last_name}",
                "mentorName": f"{job.mentor_first_name} {job.mentor_last_name}"
            }
            for job in jobs
        ]
        return {"status": "success", "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def apply_for_job_logic(user_id: int,application:ApplicationInternSchema, db: Session):

    try:
        intern_id = db.query(Intern).filter(Intern.user_id == user_id).first().id
        if not intern_id :
            raise HTTPException(status_code=404, detail="Intern not found")

        job = db.query(Job).filter(Job.id == application.jobId).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if not job.mentor_id:
            raise HTTPException(status_code=404,detail="Mentor is not assigned to project")
        if application.status != "Applied":
            raise HTTPException(status_code=400, detail="Invalid Status:"+application.status)

        already_applied = db.query(InternApplications).filter(
            InternApplications.intern_id == intern_id,
            InternApplications.job_id == application.jobId
        ).first()

        if already_applied:
            raise HTTPException(
                status_code=400,
                detail="You have already applied for this job"
            )

        new_application = InternApplications(
            status = application.status,
            job_id = application.jobId,
            mentor_id = job.mentor_id,
            intern_id = intern_id
        )

        # Add and commit the new application to the database
        db.add(new_application)
        db.commit()

        # Refresh the instance to get the latest state from the database
        db.refresh(new_application)

        # Format the response data with camelCase keys
        response_data = {
            "status": new_application.status,
            "job_id": new_application.job_id,
            "mentor_id": new_application.mentor_id,
            "intern_id": new_application.intern_id
        }

        # Return the formatted response with HTTP 200 OK status
        return {"status": "success", "data": response_data}, 200

    except Exception as e:
        # Handle any exceptions and return HTTP 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))


def view_applied_jobs_logic(user_id: int, db: Session):
    # Get intern id from user_id
    intern = db.query(Intern).filter(Intern.user_id == user_id).first()
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")

    intern_id = intern.id

    # Query applications with job and mentor details
    applications = (
        db.query(
            Job.id.label('job_id'),
            Job.title.label('job_title'),
            InternApplications.id.label("application_id"),
            InternApplications.status,
            Mentor.firstName.label('mentor_first_name'),
            Mentor.lastName.label('mentor_last_name')
        )
        .join(
            InternApplications,
            InternApplications.job_id == Job.id
        )
        .join(
            Mentor,
            Mentor.id == Job.mentor_id
        )
        .filter(InternApplications.intern_id == intern_id)
        .all()
    )

    # Format the results
    result = [
        {
            "job_id": app.job_id,
            "job_title": app.job_title,
            "application_id": app.application_id,
            "application_status": app.status,
            "mentor": f"{app.mentor_first_name} {app.mentor_last_name}"
        }
        for app in applications
    ]

    return result

def withdraw_intern_application(user_id: int, application_id: int, db: Session):
    try:

        intern_id = db.query(Intern).filter(Intern.user_id == user_id).first().id
        if not intern_id:
            raise HTTPException(status_code=404, detail="Intern not found")

        # Find the application
        application = db.query(InternApplications).filter(
            InternApplications.id == application_id,
            InternApplications.intern_id == intern_id
        ).first()

        if not application:
            raise HTTPException(
                status_code=404,
                detail="Application not found or you don't have permission to withdraw it"
            )

        # Check if application can be withdrawn (only if status is "Applied")
        if application.status != "Applied":
            raise HTTPException(
                status_code=400,
                detail="Cannot withdraw application with status: " + application.status
            )

        # Delete the application
        db.delete(application)
        db.commit()

        return {
            "status": "success",
            "message": "Application withdrawn successfully"
        }, 200

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_assigned_tasks(user_id: int, db: Session):
    """
    Retrieve all tasks assigned to the specific mentor.
    """
    intern_id = db.query(Intern).filter(Intern.user_id == user_id).first().id

    tasks = db.query(Tasks).filter(Tasks.intern_id == intern_id).all()

    # If no tasks are found, raise HTTPException
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    return tasks

def apply_for_task_review(user_id :int,task_id:int, db : Session) :
    try:
        intern_id = db.query(Intern).filter(Intern.user_id == user_id).first().id
        if not intern_id:
            raise HTTPException(status_code=404, detail="Intern not found")
        task = db.query(Tasks).filter(Tasks.intern_id == intern_id,Tasks.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status == "COMPLETE":
            raise HTTPException(status_code=404, detail="Task already completed.")
        task.status = "REVIEW"
        db.commit()
        db.refresh(task)

        return {"status": "success", "data": task}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))























def review_contract_logic(contract_id: int, db: Session):
    raise HTTPException(status_code=501, detail="Feature not yet implemented.")


def accept_contract_logic(contract_id: int, intern_id: int, db: Session):
    raise HTTPException(status_code=501, detail="Feature not yet implemented.")


def submit_milestone_logic(milestone_id: int, details: str, db: Session, intern_id: int):
    raise HTTPException(status_code=501, detail="Feature not yet implemented.")


def view_reviews_logic(intern_id: int, db: Session):
    raise HTTPException(status_code=501, detail="Feature not yet implemented.")


def get_job_application_status_logic(intern_id: int, job_id: int, db: Session):
    raise HTTPException(status_code=501, detail="Feature not yet implemented.")
