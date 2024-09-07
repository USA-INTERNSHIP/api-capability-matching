from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models.hiring_manager_model import HiringManager, Job  # Correct import
from schemas.hiring_manager_schema import HiringManagerProfileSchema, JobSchema
from sqlalchemy import or_
import json  # Add this import at the top of your file



def getHiringManagerDTO(profile:HiringManagerProfileSchema):
    res = dict()
    res["name"] = profile.name
    res['mobileNo'] = profile.mobileNo
    res['bio'] = profile.bio
    res['socialMedia'] = profile.socialMedia
    res['roleApproval'] = profile.roleApproval
    res['idDetails'] = {'idProofName': profile.idProofName, 'idProofNo': profile.idProofNo,'idProofLink': profile.idProofLink}
    res['company'] = {'companyName': profile.companyName, 'companyAddress': profile.companyAddress}
    return res

def update_hiring_manager_profile(hiring_manager_id,profile:HiringManagerProfileSchema, db: Session):
    try:
        hiringManager = db.query(HiringManager).filter(HiringManager.user_id == hiring_manager_id).first()
        if not hiringManager:
            raise HTTPException(status_code=404, detail="Hiring manager not found")
        if profile.name is not None:
            hiringManager.name = profile.name
        if profile.mobileNo is not None:
            hiringManager.mobileNo = profile.mobileNo
        if profile.bio is not None:
            hiringManager.bio = profile.bio
        if profile.socialMedia is not None:
            hiringManager.socialMedia = profile.socialMedia
        if profile.roleApproval is not None:
            hiringManager.roleApproval = profile.roleApproval

        if profile.idDetails:
            if profile.idDetails.idProofName is not None:
                hiringManager.idProofName = profile.idDetails.idProofName
            if profile.idDetails.idProofNo is not None:
                hiringManager.idProofNo = profile.idDetails.idProofNo
            if profile.idDetails.idProofLink is not None:
                hiringManager.idProofLink = profile.idDetails.idProofLink

        if profile.company:
            if profile.company.companyName is not None:
                hiringManager.companyName = profile.company.companyName
            if profile.company.companyAddress is not None:
                hiringManager.companyAddress = profile.company.companyAddress

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


def post_job_logic(job: JobSchema, db: Session, hiring_manager_id):
    """
    Logic for posting a new job by a hiring manager.
    """
    try:
        # Create a new Job instance
        new_job = Job(
            title=job.title,
            subtitle=job.subtitle,
            description=job.description,
            upload_date=job.uploadDate,  # Changed to camelCase
            deadline=job.deadline,
            stipend=job.stipend,
            duration=job.duration,
            location=job.location,
            technology_used=job.technologyUsed,  # Changed to camelCase
            hiring_manager_id=hiring_manager_id,
            approval=job.approval,
            jd_doc=job.jdDoc,  # Changed to camelCase
            perks=job.perks,
            no_of_openings=job.noOfOpenings  # Changed to camelCase
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
            "subtitle": new_job.subtitle,
            "description": new_job.description,
            "uploadDate": new_job.upload_date.isoformat(),  # Convert datetime to ISO format
            "deadline": new_job.deadline.isoformat(),  # Convert datetime to ISO format
            "stipend": new_job.stipend,
            "duration": new_job.duration,
            "location": new_job.location,
            "technologyUsed": json.loads(new_job.technology_used),  # Convert JSON string to list
            "hiringManagerId": new_job.hiring_manager_id,  # Changed to camelCase
            "approval": new_job.approval,
            "jdDoc": new_job.jd_doc,  # Changed to camelCase
            "perks": new_job.perks,
            "noOfOpenings": new_job.no_of_openings  # Changed to camelCase
        }

        # Return the formatted response with HTTP 200 OK status
        return {"status": "success", "data": response_data}, 200

    except Exception as e:
        # Handle any exceptions and return HTTP 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))


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
                Job.location.like(f"%{query}%")
            )
        ).all()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
                "subtitle": job.subtitle,
                "description": job.description,
                "uploadDate": job.upload_date.isoformat(),
                "deadline": job.deadline.isoformat(),
                "stipend": job.stipend,
                "duration": job.duration,
                "location": job.location,
                "technologyUsed": json.loads(job.technology_used),
                "hiringManagerId": job.hiring_manager_id,
                "approval": job.approval,
                "jdDoc": job.jd_doc,
                "perks": job.perks,
                "noOfOpenings": job.no_of_openings
            }
            for job in jobs
        ]
        return {"status": "success", "data": response_data}
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