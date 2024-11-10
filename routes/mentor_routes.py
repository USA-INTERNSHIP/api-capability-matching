from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.repository.mentor_repository import retrieve_mentor_profile, update_mentor_profile, apply_for_project
from db.repository.user_repository import get_userid_by_email
from db.session import get_db
from routes.auth import check_roles, verify_token
from schemas.application_schemas import ApplicationMentorSchema
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

@mentor_routes.post("/apply_for_project")
@check_roles(["MENTOR"])
def apply_for_job(application:ApplicationMentorSchema,current_user:dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = get_userid_by_email(db,current_user['user'])
    return apply_for_project(user_id,application,db)
