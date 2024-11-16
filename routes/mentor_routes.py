from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.repository.mentor_repository import retrieve_mentor_profile, update_mentor_profile, apply_for_project, \
    view_job_applications, view_available_mentor_jobs, withdraw_mentor_application, get_interesed_interns_for_project, \
    search_intern_logic, grant_intern_for_project
from db.repository.user_repository import get_userid_by_email
from db.session import get_db
from routes.auth import check_roles, verify_token
from schemas.application_schemas import ApplicationMentorSchema, InternModifyApplications
from schemas.mentor_schema import MentorProfileSchema

mentor_routes = APIRouter()

@mentor_routes.get("/profile")
@check_roles(["MENTOR"])
def get_hiring_manager_profile(current_user:dict = Depends(verify_token),db:Session=Depends(get_db)):
    mentor_id = get_userid_by_email(db,current_user['user'])
    return retrieve_mentor_profile(mentor_id, db)


@mentor_routes.put("/update_mentor_profile")
@check_roles(["MENTOR"])
def update_mentor(profile: MentorProfileSchema,current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db,current_user['user'])
    return update_mentor_profile(user_id,profile,db)

@mentor_routes.get("/view_jobs")
@check_roles(["MENTOR"])
def view_jobs(current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db,current_user['user'])
    return view_available_mentor_jobs(user_id,db)
@mentor_routes.post("/apply_for_project")
@check_roles(["MENTOR"])
def apply_for_job(application:ApplicationMentorSchema,current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db,current_user['user'])
    return apply_for_project(user_id,application,db)

@mentor_routes.get("/view_job_applications")
@check_roles(["MENTOR"])
def view_application(current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db,current_user['user'])
    return view_job_applications(user_id,db)

@mentor_routes.delete("/withdraw_application/{application_id}")
@check_roles(["MENTOR"])
def withdraw_application(application_id,current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db,current_user['user'])
    return withdraw_mentor_application(user_id,application_id,db)

@mentor_routes.get("/show_interested_interns/{project_id}")
@check_roles(["MENTOR"])
def show_interested_intern_for_project(project_id,current_user:dict = Depends(verify_token),db:Session=Depends(get_db)):
    user_id = get_userid_by_email(db, current_user['user'])
    return get_interesed_interns_for_project(project_id,user_id,db)

@mentor_routes.get("/search_intern/{intern_id}")
def search_interns(intern_id: int, current_user:dict = Depends(verify_token),db: Session = Depends(get_db)):
    return search_intern_logic(intern_id, db)

@mentor_routes.put("/modify_intern_applications")
@check_roles(["MENTOR"])
def review_applications(payload:InternModifyApplications,current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db, current_user['user'])
    return grant_intern_for_project(payload,user_id, db)
