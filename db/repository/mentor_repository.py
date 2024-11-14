import json

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session, join

from db.models import Mentor, MentorApplications, Job, HiringManager
from db.models.user_model import Users
from schemas.application_schemas import ApplicationMentorSchema
from schemas.mentor_schema import MentorProfileSchema


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
        mentor = db.query(Mentor).filter(Mentor.user_id == user_id).first()
        if mentor.id != application.mentorId:
            raise HTTPException(status_code=404, detail="Mentor not found")

        job = db.query(Job).filter(Job.id == application.jobId).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        if application.status != "Applied":
            raise HTTPException(status_code=400, detail="Invalid Status:"+application.status)

        already_applied = db.query(MentorApplications).filter(
            MentorApplications.mentor_id == application.mentorId,
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
            mentor_id = application.mentorId,
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
            "application_status": app.status,
            "hiring_manager": f"{app.hiring_manager_first_name} {app.hiring_manager_last_name}"
        }
        for app in applications
    ]

    return result