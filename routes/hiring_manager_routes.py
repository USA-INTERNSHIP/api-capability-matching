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
    read_reviews_logic, get_jobs, update_job_logic
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

@hiring_manager_routes.put("/update_job/{job_id}")
@check_roles(["HIRING_MANAGER"])  # Ensure that only hiring managers can access this endpoint
def update_job(
    job_id: int,  # Include the job_id parameter
    job: JobSchema,  # The job data to be updated
    current_user: dict = Depends(verify_token),  # Dependency to verify the current user
    db: Session = Depends(get_db)  # Dependency to get the database session
):
    hiring_manager_id = get_userid_by_email(db, current_user['user'])  # Get the hiring manager ID from the email
    try:
        # Call the logic function with the necessary parameters, including job_id
        response = update_job_logic(job_id, job, db, hiring_manager_id)  # Pass job_id to the update logic
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Raise an HTTP exception in case of error


@hiring_manager_routes.get("/search_job")
@check_roles(["HIRING_MANAGER"])  # Ensure that only hiring managers can access this endpoint
def search_job(
    query: str,
    current_user: dict = Depends(verify_token),  # Verify the current user
    db: Session = Depends(get_db)  # Accepts the database session for querying
):
    """
    Search for jobs based on a query string provided by the hiring manager.

    Parameters:
    - query (str): The search term used to find relevant jobs.
    - current_user (dict): The currently authenticated user information.
    - db (Session): The database session used for querying the database.

    Returns:
    - A list of jobs that match the search criteria, or an error if no jobs are found.
    """
    try:
        # You can log or check the user information if needed
        # Example: print(current_user) or log to a logging system

        # Call the search logic function with the provided query and database session
        response = search_job_logic(query, db)

        # Check if any jobs were found
        if not response:  # If no jobs match the query
            raise HTTPException(status_code=404, detail="No jobs found matching the query.")

        # Return the list of matching jobs with HTTP 200 OK status
        return {"status": "success", "data": response}, 200

    except Exception as e:
        # Handle any exceptions and return HTTP 400 Bad Request with the error detail
        raise HTTPException(status_code=400, detail=str(e))


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
