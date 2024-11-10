from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from db.repository.user_repository import get_userid_by_email
from db.session import get_db
from routes.auth import verify_token, check_roles
from schemas.intern_schema import (
    InternProfileSchema, ApplicationSchema, ContractSchema,
    ReviewSchema
)
from db.repository.intern_repository import (
    update_intern_profile, retrieve_intern_profile, apply_for_job_logic,
    view_available_jobs_logic, view_applied_jobs_logic, review_contract_logic,
    accept_contract_logic, submit_milestone_logic, view_reviews_logic,
    get_job_application_status_logic
)

# Initialize the APIRouter for intern-related routes
intern_routes = APIRouter()

# Route to retrieve the intern's profile
@intern_routes.get("/profile")
@check_roles(["INTERN"])
def get_intern_profile(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return retrieve_intern_profile(intern_id, db)


@intern_routes.put("/update_intern_profile")
@check_roles(["INTERN"])
def update_intern_profile_route(intern_data: InternProfileSchema, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db, current_user['user'])

    # Convert skills, idDetails, and company to JSON strings if they're present
    intern_data.skills = json.dumps(intern_data.skills) if isinstance(intern_data.skills, list) else json.dumps([])
    intern_data.idDetails = json.dumps(intern_data.idDetails) if isinstance(intern_data.idDetails, dict) else json.dumps({})
    intern_data.company = json.dumps(intern_data.company) if isinstance(intern_data.company, dict) else json.dumps({})

    # Call the update profile function
    updated_profile = update_intern_profile(user_id, intern_data, db)

    # Deserialize fields only if they are stored as JSON strings, otherwise keep them as-is
    if isinstance(updated_profile['data']['skills'], str):
        updated_profile['data']['skills'] = json.loads(updated_profile['data']['skills'])

    if isinstance(updated_profile['data']['idDetails'], str):
        updated_profile['data']['idDetails'] = json.loads(updated_profile['data']['idDetails'])

    if isinstance(updated_profile['data']['company'], str):
        updated_profile['data']['company'] = json.loads(updated_profile['data']['company'])

    return updated_profile


@intern_routes.get("/view_jobs")
@check_roles(["INTERN"])
def view_available_jobs(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    return view_available_jobs_logic(db)

# Route to allow an intern to apply for a job
@intern_routes.post("/apply_job")
@check_roles(["INTERN"])
def apply_for_job(job_application: ApplicationSchema, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return apply_for_job_logic(job_application, db, intern_id)

# Route to view all available jobs for interns

# Route to view jobs that the intern has applied for
@intern_routes.get("/applied_jobs")
@check_roles(["INTERN"])
def view_applied_jobs(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return view_applied_jobs_logic(intern_id, db)

# Route to check the status of a specific job application
@intern_routes.get("/job_application_status/{job_id}")
@check_roles(["INTERN"])
def get_job_application_status(job_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return get_job_application_status_logic(intern_id, job_id, db)

# Route to review a specific contract
@intern_routes.get("/review_contract/{contract_id}")
@check_roles(["INTERN"])
def review_contract(contract_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return review_contract_logic(contract_id, db)

# Route to accept a contract
@intern_routes.post("/accept_contract/{contract_id}")
@check_roles(["INTERN"])
def accept_contract(contract_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return accept_contract_logic(contract_id, intern_id, db)

# Route to submit a milestone
@intern_routes.post("/submit_milestone/{milestone_id}")
@check_roles(["INTERN"])
def submit_milestone(milestone_id: int, details: str, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return submit_milestone_logic(milestone_id, details, db, intern_id)

# Route to view reviews of the intern
@intern_routes.get("/view_reviews")
@check_roles(["INTERN"])
def view_reviews(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    intern_id = get_userid_by_email(db, current_user['user'])
    return view_reviews_logic(intern_id, db)
