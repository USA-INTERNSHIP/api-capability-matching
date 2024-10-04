from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models.hiring_manager_model import HiringManager, Job  # Correct import
from schemas.hiring_manager_schema import HiringManagerProfileSchema, JobSchema
from sqlalchemy import or_
import json  # Add this import at the top of your file



def getHiringManagerDTO(profile:HiringManagerProfileSchema):
    res = dict()
    res["firstName"] = profile.firstName
    res["lastName"] = profile.lastName
    res['mobileNo'] = profile.mobileNo
    return res

def update_hiring_manager_profile(hiring_manager_id,profile:HiringManagerProfileSchema, db: Session):
    try:
        hiringManager = db.query(HiringManager).filter(HiringManager.user_id == hiring_manager_id).first()
        if not hiringManager:
            raise HTTPException(status_code=404, detail="Hiring manager not found")

        if profile.firstName is not None:
            hiringManager.firstName = profile.firstName
        if profile.lastName is not None:
            hiringManager.lastName = profile.lastName
        if profile.mobileNo is not None:
            hiringManager.mobileNo = profile.mobileNo
        # if profile.socialMedia is not None:
        #     hiringManager.socialMedia = profile.socialMedia
        # if profile.roleApproval is not None:
        #     hiringManager.roleApproval = profile.roleApproval
        #
        # if profile.idDetails:
        #     if profile.idDetails.idProofName is not None:
        #         hiringManager.idProofName = profile.idDetails.idProofName
        #     if profile.idDetails.idProofNo is not None:
        #         hiringManager.idProofNo = profile.idDetails.idProofNo
        #     if profile.idDetails.idProofLink is not None:
        #         hiringManager.idProofLink = profile.idDetails.idProofLink
        #
        # if profile.company:
        #     if profile.company.companyName is not None:
        #         hiringManager.companyName = profile.company.companyName
        #     if profile.company.companyAddress is not None:
        #         hiringManager.companyAddress = profile.company.companyAddress

        db.commit()
        db.refresh(hiringManager)
        return {"status":"success","data":getHiringManagerDTO(hiringManager)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_hiring_manager_profile(hiring_manager_id, db:Session):
    profile =  db.query(HiringManager).filter(HiringManager.user_id == hiring_manager_id).first()
    if profile:
        return {"status":"success","data":getHiringManagerDTO(profile)}
    else:
        return profile


def get_jobs(hiring_manager_id: int, db: Session):
    try:
        hiring_manager = db.query(HiringManager).filter(HiringManager.user_id == hiring_manager_id).first()
        if not hiring_manager:
            raise HTTPException(status_code=404, detail="Hiring manager not found")

        jobs = db.query(Job).filter(Job.hiring_manager_id == hiring_manager_id).all()
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
                # "subtitle": job.subtitle,
                # "uploadDate": job.upload_date.isoformat(),
                # "deadline": job.deadline.isoformat(),
                # "stipend": job.stipend,
                # "location": job.location,
                # "approval": job.approval,
                # "jdDoc": job.jd_doc,
                # "perks": job.perks,
                # "noOfOpenings": job.no_of_openings
            }
            for job in jobs
        ]
        return {"status": "success", "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def post_job_logic(job: JobSchema, db: Session, hiring_manager_id):
    """
    Logic for posting a new job by a hiring manager.
    """
    try:
        # Create a new Job instance
        new_job = Job(
            title=job.title,
            technologyUsed=job.technologyUsed,
            scope = job.scope,
            description=job.description,
            budget=job.budget,
            duration=job.duration,
            hiring_manager_id=hiring_manager_id

            # subtitle=job.subtitle,
            # upload_date=job.uploadDate,  # Changed to camelCase
            # deadline=job.deadline,
            # stipend=job.stipend,
            # location=job.location,
            # approval=job.approval,
            # jd_doc=job.jdDoc,  # Changed to camelCase
            # perks=job.perks,
            # no_of_openings=job.noOfOpenings
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

            # "subtitle": new_job.subtitle,
            # "uploadDate": new_job.upload_date.isoformat(),  # Convert datetime to ISO format
            # "deadline": new_job.deadline.isoformat(),  # Convert datetime to ISO format
            # "stipend": new_job.stipend,
            # "location": new_job.location,
            # "approval": new_job.approval,
            # "jdDoc": new_job.jd_doc,  # Changed to camelCase
            # "perks": new_job.perks,
            # "noOfOpenings": new_job.no_of_openings
        }

        # Return the formatted response with HTTP 200 OK status
        return {"status": "success", "data": response_data}, 200

    except Exception as e:
        # Handle any exceptions and return HTTP 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))
    # Changed to camelCase


def search_job_logic(query: str, db: Session):

    # Important note:  If you switch to a different database (like PostgreSQL),
    # you might need to switch back to ilike for proper case-insensitive matching.
    # We need to use ilike for postgres sql database
    # e.g.Job.title.ilike(f"%{query}%"),

    try:
        jobs = db.query(Job).filter(
            or_(
                Job.title.like(f"%{query}%"),
                Job.description.like(f"%{query}%"),
                # Job.location.like(f"%{query}%")
            )
        ).all()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



#  other logic functions

# Note for my future understanding : logic for all the functions is yet to be defined as per the requirement

def search_interns_logic():
    return None


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