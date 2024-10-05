from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.repository.user_repository import get_userid_by_email
from db.session import get_db
from routes.auth import verify_token
from routes.auth import check_roles
from schemas.hiring_manager_schema import (
    HiringManagerProfileSchema, JobSchema, ApplicationSchema,
    ReviewSchema, ContractSchema
)
from db.repository.hiring_manager_repository import (
    update_hiring_manager_profile, retrieve_hiring_manager_profile, post_job_logic,
    search_job_logic, search_interns_logic, review_applications_logic,
    respond_to_interns_logic, post_contract_logic, respond_to_milestones_logic,
    pay_intern_logic, review_payment_history_logic, post_review_logic,
    read_reviews_logic, get_jobs
)

hiring_manager_routes = APIRouter()

@hiring_manager_routes.get("/profile")
@check_roles(["HIRING_MANAGER"])
def get_hiring_manager_profile(current_user:dict = Depends(verify_token),db:Session=Depends(get_db)):
    hiring_manager_id = get_userid_by_email(db,current_user['user'])
    return retrieve_hiring_manager_profile(hiring_manager_id, db)


@hiring_manager_routes.post("/update_hiring_manager_profile")
@check_roles(["HIRING_MANAGER"])
def update_hiring_manager(profile: HiringManagerProfileSchema,current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    hiring_manager_id = get_userid_by_email(db,current_user['user'])
    return update_hiring_manager_profile(hiring_manager_id,profile,db)

@hiring_manager_routes.post("/post_job")
@check_roles(["HIRING_MANAGER"])
def post_job(job: JobSchema,current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    hiring_manager_id = get_userid_by_email(db,current_user['user'])
    return post_job_logic(job, db, hiring_manager_id)

@hiring_manager_routes.get("/get_jobs")
@check_roles(["HIRING_MANAGER"])
async def get_jobs_endpoint(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    hiring_manager_id = get_userid_by_email(db, current_user['user'])
    return get_jobs(hiring_manager_id, db)

@hiring_manager_routes.get("/search_job")
def search_job(query: str, db: Session = Depends(get_db)):
    return search_job_logic(query, db)

@hiring_manager_routes.get("/search_interns")
def search_interns(query: str, db: Session = Depends(get_db)):
    return search_interns_logic(query, db)

@hiring_manager_routes.get("/review_applications")
def review_applications(job_id: int, db: Session = Depends(get_db)):
    return review_applications_logic(job_id, db)

@hiring_manager_routes.post("/respond_to_interns")
def respond_to_interns(application_id: int, response: str, db: Session = Depends(get_db)):
    return respond_to_interns_logic(application_id, response, db)

@hiring_manager_routes.post("/post_contracts")
def post_contracts(contract: ContractSchema, db: Session = Depends(get_db)):
    return post_contract_logic(contract, db)

@hiring_manager_routes.post("/respond_to_milestones")
def respond_to_milestones(contract_id: int, milestone_id: int, response: str, db: Session = Depends(get_db)):
    return respond_to_milestones_logic(contract_id, milestone_id, response, db)

@hiring_manager_routes.post("/pay_intern")
def pay_intern(intern_id: int, amount: float, db: Session = Depends(get_db)):
    return pay_intern_logic(intern_id, amount, db)

@hiring_manager_routes.get("/review_payment_history")
def review_payment_history(hiring_manager_id: int, db: Session = Depends(get_db)):
    return review_payment_history_logic(hiring_manager_id, db)

@hiring_manager_routes.post("/post_review")
def post_review(review: ReviewSchema, db: Session = Depends(get_db)):
    return post_review_logic(review, db)

@hiring_manager_routes.get("/read_reviews")
def read_reviews(hiring_manager_id: int, db: Session = Depends(get_db)):
    return read_reviews_logic(hiring_manager_id, db)
