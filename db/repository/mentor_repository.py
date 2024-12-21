import json
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, join

from db.models import Mentor, MentorApplications, Job, HiringManager, Intern, InternApplications, Tasks
from db.models.user_model import Users
from db.repository.intern_repository import get_intern_dto
from schemas.application_schemas import ApplicationMentorSchema, InternModifyApplications
from schemas.mentor_schema import MentorProfileSchema
from schemas.tasks_schema import TaskSchema


def getMentorDTO(profile:MentorProfileSchema):
    res = dict()
    res["firstName"] = profile.firstName
    res["lastName"] = profile.lastName
    res['mobileNo'] = profile.mobileNo
    return res


def retrieve_mentor_profile(user_id, db:Session):
    profile =  db.query(Mentor).filter(Mentor.user_id ==user_id).first()
    if profile:
        user = db.query(Users).filter(Users.id == profile.user_id).first()
        profile = getMentorDTO(profile)
        profile.update({"email":user.email})
        return {"data":profile}
    else:
        return profile


def view_available_mentor_jobs(user_id, db: Session):
    try:
        mentor = db.query(Mentor).filter(Mentor.user_id == user_id).first()
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")

        mentor_id = mentor.id

        # Query with explicit joins and column selection
        jobs = (
            db.query(
                Job.id,
                Job.title,
                Job.technologyUsed,
                Job.scope,
                Job.description,
                Job.duration,
                Job.budget,
                HiringManager.firstName.label('hiring_manager_first_name'),
                HiringManager.lastName.label('hiring_manager_last_name'),
                HiringManager.mobileNo.label('hiring_manager_mobile')
            )
            # Join with HiringManager table
            .join(
                HiringManager,
                Job.hiring_manager_id == HiringManager.id
            )
            # Left join with MentorApplications to check if mentor has already applied
            .outerjoin(
                MentorApplications,
                and_(
                    MentorApplications.job_id == Job.id,
                    MentorApplications.mentor_id == mentor_id,
                    MentorApplications.status == "Applied"
                )
            )
            # Filter conditions:
            # 1. Jobs where no mentor is assigned
            # 2. Jobs where the mentor hasn't already applied
            .filter(
                and_(
                    Job.mentor_id.is_(None),
                    MentorApplications.id.is_(None)
                )
            )
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
                "budget": job.budget,
                "hiringManager": {
                    "name": f"{job.hiring_manager_first_name} {job.hiring_manager_last_name}",
                    "mobile": job.hiring_manager_mobile
                }
            }
            for job in jobs
        ]
        return {"status": "success", "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_mentor_profile(user_id, profile: MentorProfileSchema, db: Session):
    try:
        mentor = db.query(Mentor).filter(Mentor.user_id == user_id).first()
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor not found")

        if profile.firstName is not None:
            mentor.firstName = profile.firstName
        if profile.lastName is not None:
            mentor.lastName = profile.lastName
        if profile.mobileNo is not None:
            mentor.mobileNo = profile.mobileNo

        db.commit()
        db.refresh(mentor)
        return {"status": "success", "data": getMentorDTO(mentor)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def apply_for_project(user_id:int,application:ApplicationMentorSchema,db:Session):

    try:
        mentor_id = db.query(Mentor).filter(Mentor.user_id == user_id).first().id
        if not mentor_id :
            raise HTTPException(status_code=404, detail="Mentor not found")

        job = db.query(Job).filter(Job.id == application.jobId).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if application.status != "Applied":
            raise HTTPException(status_code=400, detail="Invalid Status:"+application.status)

        already_applied = db.query(MentorApplications).filter(
            MentorApplications.mentor_id == mentor_id,
            MentorApplications.job_id == application.jobId
        ).first()

        if already_applied:
            raise HTTPException(
                status_code=400,
                detail="You have already applied for this job"
            )

        new_application = MentorApplications(
            status = application.status,
            job_id = application.jobId,
            mentor_id = mentor_id,
            hiring_manager_id = job.hiring_manager.id
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
            "hiring_manager_id": new_application.hiring_manager_id
        }

        # Return the formatted response with HTTP 200 OK status
        return {"status": "success", "data": response_data}, 200

    except Exception as e:
        # Handle any exceptions and return HTTP 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))


def view_job_applications(user_id: int, db: Session):
    # Get mentor id from user_id
    mentor = db.query(Mentor).filter(Mentor.user_id == user_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    mentor_id = mentor.id

    # Query applications with job and hiring manager details
    applications = (
        db.query(
            Job.id.label('job_id'),
            Job.title.label('job_title'),
            MentorApplications.id.label("application_id"),
            MentorApplications.status,
            HiringManager.firstName.label('hiring_manager_first_name'),
            HiringManager.lastName.label('hiring_manager_last_name')
        )
        .join(
            MentorApplications,
            MentorApplications.job_id == Job.id
        )
        .join(
            HiringManager,
            HiringManager.id == Job.hiring_manager_id
        )
        .filter(MentorApplications.mentor_id == mentor_id)
        .all()
    )

    # Format the results
    result = [
        {
            "job_id": app.job_id,
            "job_title": app.job_title,
            "application_id":app.application_id,
            "application_status": app.status,
            "hiring_manager": f"{app.hiring_manager_first_name} {app.hiring_manager_last_name}"
        }
        for app in applications
    ]

    return result


def withdraw_mentor_application(user_id: int, application_id: int, db: Session):
    try:

        mentor_id = db.query(Mentor).filter(Mentor.user_id == user_id).first().id
        if not mentor_id:
            raise HTTPException(status_code=404, detail="Mentor not found")

        # Find the application
        application = db.query(MentorApplications).filter(
            MentorApplications.id == application_id,
            MentorApplications.mentor_id == mentor_id
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

def get_interesed_interns_for_project(project_id,user_id,db:Session):
    mentor_id = db.query(Mentor).filter(Mentor.user_id == user_id).first().id

    project = db.query(Job).filter(Job.id == project_id,Job.mentor_id == mentor_id).first()
    if not project:
        raise HTTPException(status_code=404,detail="Project not found or you don't have access to this project.")

    intern_applications = (
        db.query(
            Intern.firstName,
            Intern.lastName,
            Intern.mobileNo,
            InternApplications.id,
            InternApplications.job_id,
            Intern.id,
            InternApplications.status
        )
        .join(InternApplications,
              and_(
                  InternApplications.intern_id == Intern.id,
                  or_(
                      InternApplications.status == "Applied"
                  )
              )).filter(InternApplications.job_id == project_id)
        .all()
    )
    result = [
        {
            "firstName": intern[0],
            "lastName": intern[1],
            "mobile_no": intern[2],
            "application_id":intern[3],
            "job_id":intern[4],
            "intern_id":intern[5],
            "application_status":intern[6]
        }
        for intern in intern_applications
    ]
    return result

def search_intern_logic(intern_id:int,db:Session):
    profile = db.query(Intern).filter(Intern.id == intern_id).first()
    if profile:
        # Deserialize JSON fields before returning the DTO
        profile.skills = json.loads(profile.skills) if profile.skills else []
        profile.idDetails = json.loads(profile.idDetails) if profile.idDetails else {}
        profile.company = json.loads(profile.company) if profile.company else {}
        # user = db.query(Users).filter(Users.id == profile.user_id).first()
        profile = get_intern_dto(profile)
        # profile.update({"email": user.email})
        return {"status": "success", "data": profile}
    else:
        raise HTTPException(status_code=404, detail="Intern not found")

def grant_intern_for_project(payload: InternModifyApplications, user_id: int, db: Session):
    # First verify if the application exists and belongs to the mentor
    application = db.query(InternApplications).filter(
        InternApplications.id == payload.applicationId,
        InternApplications.intern_id == payload.internId
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found or invalid intern ID"
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
    mentor_id = db.query(Mentor).filter(Mentor.user_id == user_id).first().id
    job = db.query(Job).filter(
        Job.id == payload.jobId,
        Job.mentor_id == mentor_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found or you don't have access"
        )

    try:
        if payload.status == "Approved":
            # Update the accepted application
            application.status = "Approved"
        elif payload.status == "Rejected":
            # update the status to rejected for this application
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

def get_interns_for_project(project_id,user_id,db:Session):

    mentor_id = db.query(Mentor).filter(Mentor.user_id == user_id).first().id

    project = db.query(Job).filter(Job.id == project_id,Job.mentor_id == mentor_id).first()
    if not project:
        raise HTTPException(status_code=404,detail="Project not found or you don't have access to this project.")

    intern_applications = (
        db.query(
            Intern.firstName,
            Intern.lastName,
            Intern.id,
        )
        .join(InternApplications,
              and_(
                  InternApplications.intern_id == Intern.id,
                  or_(
                      InternApplications.status == "Approved"
                  )
              )).filter(InternApplications.job_id == project_id)
        .all()
    )
    result = [
        {
            "Name": f"{intern[0]} {intern[1]}",
            "job_id":project.id,
            "intern_id":intern[2],
        }
        for intern in intern_applications
    ]
    return result


def create_task_for_intern(task: TaskSchema, user_id: int, db: Session):
    try:
        # Get mentor id from user_id
        mentor = db.query(Mentor).filter(Mentor.user_id == user_id).first()
        if not mentor:
            raise HTTPException(
                status_code=404,
                detail="Mentor not found or you don't have access to this project."
            )

        mentor_id = mentor.id

        # Check if application exists and is approved
        application = db.query(InternApplications).filter(
            InternApplications.job_id == task.job_id,
            InternApplications.intern_id == task.intern_id,
            InternApplications.mentor_id == mentor_id,
            InternApplications.status == "Approved"
        ).first()

        if not application:
            raise HTTPException(
                status_code=404,
                detail="No approved application found for this intern under your mentorship"
            )

        # Create new task
        new_task = Tasks(
            title=task.title,
            status=task.status,
            description=task.description,
            attachment=task.attachment,
            assigned_date=task.assigned_date,
            due_date=task.due_date,
            completion_date=None,
            feedback=None,

            job_id=task.job_id,
            intern_id=task.intern_id,
            mentor_id=mentor_id
        )

        # Add and commit to database
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        # Create comprehensive response data
        response_data = {
            "id": new_task.id,
            "title": new_task.title,
            "status": new_task.status,
            "description": new_task.description,
            "attachment": new_task.attachment,
            "assigned_date": new_task.assigned_date,
            "due_date": new_task.due_date,
            "completion_date": new_task.completion_date,
            "feedback": new_task.feedback,
            "job_id": new_task.job_id,
            "mentor_id": new_task.mentor_id,
            "intern_id": new_task.intern_id
        }

        return {
            "status": "success",
            "message": "Task assigned successfully",
            "data": response_data
        }, 200

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the task: {str(e)}"
        )



def retrieve_task(task_id: int, db: Session):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task_details(task_id: int, task_payload: TaskSchema, db: Session):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_payload.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def update_task_status(task_id: int, status: str, db: Session):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status
    if status == "Completed":
        task.completion_date = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task



def update_task_status_to_partially_completed(task_id: int, db: Session):
    """
    Update the status of a task to 'Partially Completed' and return the updated task serialized using Pydantic.
    """
    try:
        # Find the task by its ID
        task = db.query(Tasks).filter(Tasks.id == task_id).first()

        # If task doesn't exist, raise an exception
        if not task:
            raise NoResultFound

        # Update the status of the task
        task.status = "Partially Completed"

        # Commit the changes to the database
        db.commit()

        # Return the updated task serialized as Pydantic model
        return TaskSchema.from_orm(task)  # Convert to Pydantic model

    except NoResultFound:
        return None  # Return None if the task is not found

def view_job_by_id(job_id: int, db: Session):
    """
    Fetch a job by its ID from the database.
    """
    return db.query(Job).filter(Job.id == job_id).first()


def retrieve_all_tasks(user_id: int, db: Session):
    """
    Retrieve all tasks assigned to the specific mentor.
    """
    mentor_id = db.query(Mentor).filter(Mentor.user_id == user_id).first().id

    tasks = db.query(Tasks).filter(Tasks.mentor_id == mentor_id).all()

    # If no tasks are found, raise HTTPException
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    return tasks

def retrieve_tasks_by_job(user_id: int, job_id: int, db: Session):
    """
    Retrieve all tasks assigned to the specific mentor for a specific job.
    """
    # Get the mentor ID from the user ID
    mentor = db.query(Mentor).filter(Mentor.user_id == user_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    mentor_id = mentor.id

    # Check if the job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Query tasks for the mentor and the specific job ID
    tasks = db.query(Tasks).filter(Tasks.mentor_id == mentor_id).filter(Tasks.job_id == job_id).all()

    # If no tasks are found, raise an HTTPException
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    return tasks
