from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models.hiring_manager_model import HiringManager  # Correct import
from schemas.hiring_manager_schema import  HiringManagerProfileSchema

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
        return getHiringManagerDTO(hiringManager)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def retrieve_hiring_manager_profile(hiring_manager_id, db:Session):
    profile =  db.query(HiringManager).filter(HiringManager.user_id == hiring_manager_id).first()
    if profile:
        return getHiringManagerDTO(profile)
    else:
        return profile

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