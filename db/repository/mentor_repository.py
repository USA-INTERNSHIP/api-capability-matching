from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Mentor, MentorApplications, Job
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