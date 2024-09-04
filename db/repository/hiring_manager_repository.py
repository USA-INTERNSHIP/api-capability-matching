from http.client import HTTPException

from sqlalchemy.orm import Session
from db.models.hiring_manager_model import HiringManager, Job  # Correct import
from schemas.hiring_manager_schema import  HiringManagerProfileSchema


def update_hiring_manager_profile(hiring_manager_id,profile:HiringManagerProfileSchema, db: Session):
    try:
        hiringManager = retrive_hiring_manager_profile(hiring_manager_id,db)
        if not hiringManager:
            raise HTTPException(status_code=404, detail="Hiring manager not found")

        hiringManager.name = profile.name
        hiringManager.mobileNo = profile.mobileNo
        hiringManager.bio = profile.bio
        hiringManager.socialMedia = profile.socialMedia
        hiringManager.idProofName = profile.idProofName
        hiringManager.idProofNo = profile.idProofNo
        hiringManager.companyName = profile.companyName
        hiringManager.companyAddress = profile.companyAddress

        db.commit()
        db.refresh(hiringManager)
        return hiringManager
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrive_hiring_manager_profile(hiring_manager_id,db:Session):
    return db.query(HiringManager).filter(HiringManager.user_id == hiring_manager_id).first()









def post_job_logic(job, db: Session):
    # Post a new job in the database
    pass


#  other logic functions

# Note for my future understanding : logic for all the functions is yet to be defined as per the requirement
def search_job_logic():
    return None


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