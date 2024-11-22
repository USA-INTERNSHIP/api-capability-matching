from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.repository.mentor_repository import retrieve_mentor_profile, update_mentor_profile, apply_for_project, \
    view_job_applications, view_available_mentor_jobs, withdraw_mentor_application, get_interesed_interns_for_project, \
    search_intern_logic, grant_intern_for_project, get_interns_for_project, create_task_for_intern, update_task_status, \
    update_task_details, retrieve_task, update_task_status_to_partially_completed
from db.repository.user_repository import get_userid_by_email
from db.session import get_db
from routes.auth import check_roles, verify_token
from schemas.application_schemas import ApplicationMentorSchema, InternModifyApplications
from schemas.mentor_schema import MentorProfileSchema
from schemas.tasks_schema import TaskSchema

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

@mentor_routes.get("/show_project_interns/{project_id}")
@check_roles(["MENTOR"])
def show_project_intern_for_project(project_id,current_user:dict = Depends(verify_token),db:Session=Depends(get_db)):
    user_id = get_userid_by_email(db, current_user['user'])
    return get_interns_for_project(project_id,user_id,db)

@mentor_routes.post("/assign_task_to_intern")
@check_roles(["MENTOR"])
def show_project_intern_for_project(task:TaskSchema,current_user:dict = Depends(verify_token),db:Session=Depends(get_db)):
    user_id = get_userid_by_email(db, current_user['user'])
    return create_task_for_intern(task,user_id,db)

@mentor_routes.get("/view_task/{task_id}")
@check_roles(["MENTOR"])
def view_task(task_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    task = retrieve_task(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@mentor_routes.put("/update_task/{task_id}")
@check_roles(["MENTOR"])
def update_task(task_id: int, task_payload: TaskSchema, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    return update_task_details(task_id, task_payload, db)


@mentor_routes.put("/update_task_status/{task_id}")
@check_roles(["MENTOR"])  # Ensure the user is a mentor
def update_task_status_to_partially_completed_route(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """
    Change the status of a task to 'Partially Completed'.
    This can only be performed by a mentor.
    """
    # Call the repository to update the task status
    task = update_task_status_to_partially_completed(task_id, db)

    # If task not found, raise HTTP 404 error
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Return the response with task status update message and the task serialized as Pydantic model
    return {"message": "Task status updated to 'Partially Completed'", "task": task}


@mentor_routes.patch("/mark_task_completed/{task_id}")
@check_roles(["MENTOR"])
def mark_task_completed(task_id: int, current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    return update_task_status(task_id, "Completed", db)
