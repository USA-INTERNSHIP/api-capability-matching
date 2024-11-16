from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import MentorApplications, Mentor
from db.models.hiring_manager_model import HiringManager, Job  # Correct import
from db.models.user_model import Users
from schemas.application_schemas import MentorModifyApplications
from schemas.hiring_manager_schema import HiringManagerProfileSchema, JobSchema
from sqlalchemy import or_, and_
import json  # Add this import at the top of your file



def getHiringManagerDTO(profile:HiringManagerProfileSchema):
    res = dict()
    res["firstName"] = profile.firstName
    res["lastName"] = profile.lastName
    res['mobileNo'] = profile.mobileNo
    return res

def update_hiring_manager_profile(user_id,profile:HiringManagerProfileSchema, db: Session):
    try:
        hiringManager = db.query(HiringManager).filter(HiringManager.user_id == user_id).first()
        if not hiringManager:
            raise HTTPException(status_code=404, detail="Hiring manager not found")

        if profile.firstName is not None:
            hiringManager.firstName = profile.firstName
        if profile.lastName is not None:
            hiringManager.lastName = profile.lastName
        if profile.mobileNo is not None:
            hiringManager.mobileNo = profile.mobileNo

        db.commit()
        db.refresh(hiringManager)
        return {"status":"success","data":getHiringManagerDTO(hiringManager)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_hiring_manager_profile(user_id, db:Session):
    profile =  db.query(HiringManager).filter(HiringManager.user_id == user_id).first()
    if profile:
        user = db.query(Users).filter(Users.id == profile.user_id).first()
        profile = getHiringManagerDTO(profile)
        profile.update({"email":user.email})
        return {"data":profile}
    else:
        return profile


def get_jobs(user_id: int, db: Session):
    try:
        hiring_manager = db.query(HiringManager).filter(HiringManager.user_id == user_id).first()
        if not hiring_manager:
            raise HTTPException(status_code=404, detail="Hiring manager not found")

        jobs = db.query(Job).filter(Job.hiring_manager_id == hiring_manager.id).all()
        response_data = [
            {
                "id": job.id,
                "title": job.title,
                "technologyUsed": json.loads(job.technologyUsed),
                "scope":job.scope,
                "description": job.description,
                "budget":job.budget,
                "duration": job.duration,
                "hiringManagerId": job.hiring_manager_id
            }
            for job in jobs
        ]
        return {"status": "success", "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def post_job_logic(job: JobSchema, db: Session, user_id):
    """
    Logic for posting a new job by a hiring manager.
    """
    try:
        hiring_manager_id = db.query(HiringManager).filter(HiringManager.user_id == user_id).first().id
        if not hiring_manager_id:
            raise HTTPException(status_code=404, detail="Hiring manager not found")
        # Create a new Job instance
        new_job = Job(
            title=job.title,
            technologyUsed=job.technologyUsed,
            scope = job.scope,
            description=job.description,
            budget=job.budget,
            duration=job.duration,
            hiring_manager_id=hiring_manager_id

        )

        # Add and commit the new job to the database
        db.add(new_job)
        db.commit()

        # Refresh the instance to get the latest state from the database
        db.refresh(new_job)

        # Format the response data with camelCase keys
        response_data = {
            "id": new_job.id,
            "title": new_job.title,
            "technologyUsed": json.loads(new_job.technologyUsed),  # Convert JSON string to list
            "scope":new_job.scope,
            "description": new_job.description,
            "budget":new_job.budget,
            "duration": new_job.duration,
            "hiringManagerId": new_job.hiring_manager_id,  # Changed to camelCase

        }

        # Return the formatted response with HTTP 200 OK status
        return {"status": "success", "data": response_data}, 200

    except Exception as e:
        # Handle any exceptions and return HTTP 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))
    # Changed to camelCase

def update_job_logic(job_id: int, job: JobSchema, db: Session, user_id: int):
    """
    Logic for updating an existing job by a hiring manager.

    Parameters:
    - job_id (int): The ID of the job to update.
    - job (JobSchema): The new job data provided for the update.
    - db (Session): The database session for executing queries.
    - hiring_manager_id (int): The ID of the hiring manager attempting to update the job.

    Returns:
    - A success response with updated job data if the update is successful.
    - Raises HTTPException for errors such as job not found or update failures.
    """
    try:
        hiring_manager_id = db.query(HiringManager).filter(HiringManager.user_id == user_id).first().id
        if not hiring_manager_id:
            raise HTTPException(status_code=404, detail="Hiring manager not found")
        # Retrieve the job from the database
        existing_job = db.query(Job).filter(
            Job.id == job_id,  # Filter by the job ID
            Job.hiring_manager_id == hiring_manager_id  # Ensure the job belongs to the hiring manager
        ).first()

        # Check if the job exists and if the hiring manager has permission to update it
        if not existing_job:
            raise HTTPException(status_code=404, detail="Job not found or you do not have permission to update it.")

        # Update job details if provided in the request
        if job.title is not None:  # Check if a new title is provided
            existing_job.title = job.title  # Update the title
        if job.technologyUsed is not None:  # Check if new technology is provided
            existing_job.technologyUsed = json.dumps(job.technologyUsed)  # Store as JSON string
        if job.scope is not None:  # Check if a new scope is provided
            existing_job.scope = job.scope  # Update the scope
        if job.description is not None:  # Check if a new description is provided
            existing_job.description = job.description  # Update the description
        if job.budget is not None:  # Check if a new budget is provided
            existing_job.budget = job.budget  # Update the budget
        if job.duration is not None:  # Check if a new duration is provided
            existing_job.duration = job.duration  # Update the duration

        # Add any additional fields that may need to be updated here

        # Commit the changes to the database to save updates
        db.commit()

        # Refresh the instance to get the latest state from the database
        db.refresh(existing_job)

        # Format the response data with camelCase keys for consistency
        response_data = {
            "id": existing_job.id,  # Job ID
            "title": existing_job.title,  # Job title
            "technologyUsed": json.loads(existing_job.technologyUsed),  # Convert JSON string back to list
            "scope": existing_job.scope,  # Job scope
            "description": existing_job.description,  # Job description
            "budget": existing_job.budget,  # Job budget
            "duration": existing_job.duration,  # Job duration
            "hiringManagerId": existing_job.hiring_manager_id,  # ID of the hiring manager
            # Add any additional fields that need to be included in the response here
        }

        # Return the formatted response with HTTP 200 OK status
        return {"status": "success", "data": response_data}, 200

    except Exception as e:
        # Handle any exceptions that occur during the process
        # Raise HTTP 400 Bad Request with the error detail
        raise HTTPException(status_code=400, detail=str(e))


def search_job_logic(query: str, db: Session):
    """
    Logic for searching jobs based on a query string.

    Parameters:
    - query (str): The search term used to find relevant jobs.
    - db (Session): The database session for executing queries.

    Returns:
    - A list of jobs that match the search criteria.
    - Raises HTTPException for errors during the search.


    # Important note:  If you switch to a different database (like PostgreSQL),
    # you might need to switch back to ilike for proper case-insensitive matching.
    # We need to use ilike for postgres sql database
    # e.g.Job.title.ilike(f"%{query}%"),

    """
    try:
        jobs = db.query(Job).filter(
            or_(
                Job.title.like(f"%{query}%"),  # Match title
                Job.description.like(f"%{query}%"),  # Match description
                # Job.location.like(f"%{query}%")  # Uncomment if location search is needed
            )
        ).all()  # Retrieve all matching jobs

        return jobs  # Return the list of jobs found
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle exceptions


def get_interesed_mentors_for_project(project_id,user_id,db:Session):
    hiring_manager_id = db.query(HiringManager).filter(HiringManager.user_id == user_id).first().id

    project = db.query(Job).filter(Job.id == project_id,Job.hiring_manager_id == hiring_manager_id).first()
    if not project:
        raise HTTPException(status_code=404,detail="Project not found or you don't have access to this project.")

    mentor_applications = (
        db.query(
            Mentor.firstName,
            Mentor.lastName,
            Mentor.mobileNo,
            MentorApplications.id,
            MentorApplications.job_id,
            Mentor.id,
            MentorApplications.status
        )
        .join(MentorApplications,
              and_(
                  MentorApplications.mentor_id == Mentor.id,
                  or_(
                      MentorApplications.status == "Applied",
                      MentorApplications.status == "Approved"
                  )
              )).filter(MentorApplications.job_id == project_id)
        .all()
    )
    result = [
        {
            "firstName": mentor[0],
            "lastName": mentor[1],
            "mobile_no": mentor[2],
            "application_id":mentor[3],
            "job_id":mentor[4],
            "mentor_id":mentor[5],
            "application_status":mentor[6]
        }
        for mentor in mentor_applications
    ]
    return result


def grant_mentor_for_project(payload: MentorModifyApplications, user_id: int, db: Session):
    # First verify if the application exists and belongs to the hiring manager
    application = db.query(MentorApplications).filter(
        MentorApplications.id == payload.applicationId,
        MentorApplications.mentor_id == payload.mentorId
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found or invalid mentor ID"
        )
    if application.job_id != payload.jobId:
        raise HTTPException(
            status_code=400,
            detail="Job ID in payload doesn't match with application"
        )
    if application.status == "Approved":
        raise HTTPException(
            status_code=404,
            detail="You can not modify status after Approval."
        )
    # Verify if the job belongs to this hiring manager
    hiring_manager_id = db.query(HiringManager).filter(HiringManager.user_id == user_id).first().id
    job = db.query(Job).filter(
        Job.id == payload.jobId,
        Job.hiring_manager_id == hiring_manager_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found or you don't have access"
        )

    try:
        if payload.status == "Approved":
            # Update all other applications for this job to rejected
            db.query(MentorApplications).filter(
                MentorApplications.job_id == payload.jobId,
                MentorApplications.id != payload.applicationId
            ).update({"status": "Rejected"})

            # Update the accepted application
            application.status = "Approved"

            # Update job table with selected mentor
            job.mentor_id = payload.mentorId

        elif payload.status == "Rejected":
            # Just update the status to rejected for this application
            application.status = "Rejected"
        else:
            raise HTTPException(
                status_code=404,
                detail="Invalid Job Status"
            )
        db.commit()
        db.refresh(job)
        db.refresh(application)
        return application

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating application: {str(e)}"
        )

# Note for my future understanding : logic for all the functions is yet to be defined as per the requirement
# def search_interns_logic():
#     return None


def review_applications_logic():
    return None


def respond_to_interns_logic():
    return None


def post_contract_logic():
    return None


def respond_to_milestones_logic():
    return None


def pay_intern_logic():
    return None


def review_payment_history_logic():
    return None


def post_review_logic():
    return None


def read_reviews_logic():
    return None