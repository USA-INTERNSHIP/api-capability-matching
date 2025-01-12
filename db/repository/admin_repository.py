from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext
from fastapi import HTTPException

from db.models import Mentor, HiringManager, Job, Intern, Tasks
from db.models.user_model import Users
from db.models.admin_model import Admin
from schemas.admin_schema import AdminRegisterSchema
from schemas.user_schema import UserRegisterSchema

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin(admin: AdminRegisterSchema, db: Session):
    try:
        # Check if the email already exists
        existing_user = db.query(Users).filter(Users.email == admin.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=f"User with email '{admin.email}' already exists."
            )

        # Hash the password
        hashed_password = pwd_context.hash(admin.password)

        # Create user object
        user_obj = Users(
            email=admin.email,
            password=hashed_password,
            username=admin.email.split('@')[0],  # Use the part before '@' as the username
            socialLogin=admin.socialLogin,
            userRole=admin.userRole,
        )

        # Add user to the database
        db.add(user_obj)
        db.commit()  # Commit to save user
        db.refresh(user_obj)  # Refresh to get the latest data

        # Logic for admin role
        if user_obj.userRole == "ADMIN":
            admin_obj = Admin(
                user_id=user_obj.id,  # Link to the created user
                username=user_obj.username,  # Use username from Users
                email=user_obj.email,  # Use email from Users
                socialLogin=user_obj.socialLogin,  # Social login status
                userRole=user_obj.userRole,  # Role explicitly set to ADMIN
            )
            db.add(admin_obj)  # Add admin to the session
            db.commit()  # Commit the session for admin
            db.refresh(admin_obj)  # Refresh if needed

        return user_obj  # Return the created user object
    except HTTPException as e:
        db.rollback()  # Rollback the session if any HTTPException occurs
        raise e
    except Exception as e:
        db.rollback()  # Rollback the session if any other error occurs
        raise HTTPException(status_code=400, detail=str(e))

def create_mentor(user:UserRegisterSchema,db:Session):
    try:
        # Check if the email already exists
        existing_user = db.query(Users).filter(Users.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=f"User with email '{user.email}' already exists."
            )
        if user.userRole != "MENTOR":
            raise HTTPException(status_code=400, detail=f"Invalid Role : '{user.userRole}")
        # Hash the password
        hashed_password = pwd_context.hash(user.password)

        # Create user object
        user_obj = Users(
            email=user.email,
            password=hashed_password,
            username=user.email.split('@')[0],  # Use the part before '@' as the username
            socialLogin=user.socialLogin,
            userRole=user.userRole,
        )

        # Add user to the database
        db.add(user_obj)
        db.commit()  # Commit to save user
        db.refresh(user_obj)  # Refresh to get the latest data

        # Logic for admin role
        if user_obj.userRole == "MENTOR":
            mentor = Mentor(
                user_id=user_obj.id,  # Link to the created user
                firstName= "Mentor",  # Explicitly set to Mentor
                lastName=None,  # Explicitly set to None, as allowed
                mobileNo=None  # Mobile number is NULL
            )
            db.add(mentor)  # Add mentor to the session
            db.commit()  # Commit the session for intern
            db.refresh(mentor)  # Refresh if needed
        return user_obj  # Return the created user object
    except HTTPException as e:
        db.rollback()  # Rollback the session if any HTTPException occurs
        raise e
    except Exception as e:
        db.rollback()  # Rollback the session if any other error occurs
        raise HTTPException(status_code=400, detail=str(e))


def get_all_hiring_managers(db: Session):
    hiring_managers = (
        db.query(HiringManager)
        .options(
            joinedload(HiringManager.user),
            joinedload(HiringManager.jobs)
        )
        .all()
    )

    result = []
    for hm in hiring_managers:
        hiring_manager_data = {
            'id': hm.id,
            'firstName': hm.firstName,
            'lastName': hm.lastName,
            'mobileNo': hm.mobileNo,
            'user': {
                'id': hm.user.id,
                'username': hm.user.username,
                'email': hm.user.email
            } if hm.user else None,
            'statistics': {
                'jobs_count': len(hm.jobs),
                'mentor_applications_count': len(hm.mentor_applications)
            }
        }
        result.append(hiring_manager_data)

    return result
def get_all_mentors(db: Session):

    mentors = (
        db.query(Mentor)
        .options(
            joinedload(Mentor.user),
            joinedload(Mentor.jobs),
            joinedload(Mentor.tasks)
        )
        .all()
    )

    result = []
    for mentor in mentors:
        mentor_data = {
            'id': mentor.id,
            'firstName': mentor.firstName,
            'lastName': mentor.lastName,
            'mobileNo': mentor.mobileNo,
            'user': {
                'id': mentor.user.id,
                'username': mentor.user.username,
                'email': mentor.user.email
            } if mentor.user else None,
            'statistics': {
                'jobs_count': len(mentor.jobs),
                'tasks_count': len(mentor.tasks),
                'mentor_applications_count': len(mentor.mentor_applications),
                'intern_applications_count': len(mentor.intern_applications)
            }
        }
        result.append(mentor_data)

    return result
def get_all_jobs(db: Session):

    jobs = (
        db.query(Job)
        .options(
            joinedload(Job.hiring_manager).joinedload(HiringManager.user),
            joinedload(Job.mentor).joinedload(Mentor.user)
        )
        .all()
    )

    result = []
    for job in jobs:
        job_data = {
            'id': job.id,
            'title': job.title,
            'technologies': job.technology_used_list,  # Uses the property to automatically decode JSON
            'scope': job.scope,
            'description': job.description,
            'budget': job.budget,
            'duration': job.duration,
            'hiring_manager': {
                'id': job.hiring_manager.id,
                'name': f"{job.hiring_manager.firstName} {job.hiring_manager.lastName}",
                'email': job.hiring_manager.user.email
            } if job.hiring_manager else None,
            'mentor': {
                'id': job.mentor.id,
                'name': f"{job.mentor.firstName} {job.mentor.lastName}",
                'email': job.mentor.user.email
            } if job.mentor else None,
            'statistics': {
                'mentor_applications_count': len(job.mentor_applications),
                'intern_applications_count': len(job.intern_applications),
                'tasks_count': len(job.tasks)
            }
        }
        result.append(job_data)

    return result


def get_all_interns(db: Session):

    interns = (
        db.query(Intern)
        .options(
            joinedload(Intern.user),
            joinedload(Intern.applications),
            joinedload(Intern.tasks)
        )
        .all()
    )

    result = []
    for intern in interns:
        intern_data = {
            'id': intern.id,
            'firstName': intern.firstName,
            'lastName': intern.lastName,
            'mobileNo': intern.mobileNo,
            'education': intern.education,
            'skills': intern.skills_list,  # Using property to decode JSON
            'status': intern.status,
            'idDetails': intern.id_details_dict,  # Using property to decode JSON
            'company': intern.company_dict,  # Using property to decode JSON
            'user': {
                'id': intern.user.id,
                'username': intern.user.username,
                'email': intern.user.email
            } if intern.user else None,
            'statistics': {
                'total_applications': len(intern.applications),
                'total_tasks': len(intern.tasks)
            }
        }
        result.append(intern_data)

    return result


def get_all_tasks(db: Session):

    tasks = (
        db.query(Tasks)
        .options(
            joinedload(Tasks.job),
            joinedload(Tasks.mentor).joinedload(Mentor.user),
            joinedload(Tasks.intern).joinedload(Intern.user)
        )
        .all()
    )

    result = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'description': task.description,
            'attachment': task.attachment,
            'dates': {
                'assigned': task.assigned_date.isoformat() if task.assigned_date else None,
                'due': task.due_date.isoformat() if task.due_date else None,
                'completion': task.completion_date.isoformat() if task.completion_date else None
            },
            'feedback': task.feedback,
            'job': {
                'id': task.job.id,
                'title': task.job.title
            } if task.job else None,
            'mentor': {
                'id': task.mentor.id,
                'name': f"{task.mentor.firstName} {task.mentor.lastName}",
                'email': task.mentor.user.email
            } if task.mentor else None,
            'intern': {
                'id': task.intern.id,
                'name': f"{task.intern.firstName} {task.intern.lastName}",
                'email': task.intern.user.email
            } if task.intern else None
        }
        result.append(task_data)

    return result