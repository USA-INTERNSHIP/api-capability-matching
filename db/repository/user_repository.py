from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.models.hiring_manager_model import HiringManager
from db.models.intern_model import Intern
from db.models.user_model import Users
from fastapi import HTTPException
from schemas.user_schema import UserRegisterSchema

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user: UserRegisterSchema, db: Session):
    try:
        # Hash the password
        hashed_password = pwd_context.hash(user.password)
        user_obj = Users(
            email=user.email,
            password=hashed_password,
            username=user.username.split('@')[0],  # Use the part before '@' as the username
            socialLogin=user.socialLogin,
            userRole=user.userRole,
        )

        # Add user to the database
        db.add(user_obj)
        db.commit()  # Commit to save user
        db.refresh(user_obj)  # Refresh to get the latest data

        # Logic for hiring manager role
        if user_obj.userRole == "HIRING_MANAGER":
            hiring_manager = HiringManager(user_id=user_obj.id)  # Link to the created user
            db.add(hiring_manager)
            db.commit()  # Commit to save hiring manager
            db.refresh(hiring_manager)  # Refresh to get the latest data

        # Logic for intern role
        elif user_obj.userRole == "INTERN":
            intern = Intern(
                user_id=user_obj.id,  # Link to the created user
                firstName=None,  # Explicitly set to None, as allowed
                lastName=None,  # Explicitly set to None, as allowed
                mobileNo=None  # Mobile number is NULL
            )
            db.add(intern)  # Add intern to the session
            db.commit()  # Commit the session for intern
            db.refresh(intern)  # Refresh if needed

        return user_obj  # Return the created user object
    except Exception as e:
        db.rollback()  # Rollback the session if any error occurs
        raise HTTPException(status_code=400, detail=str(e))

def get_users(db: Session):
    """Fetch all users from the database."""
    return db.query(Users).all()

def get_user_by_email(db: Session, email: str):
    """Fetch a user by their email address."""
    return db.query(Users).filter(Users.email == email).first()

def get_userid_by_email(db: Session, email: str) -> int:
    """Fetch user ID by email address."""
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return user.id
    else:
        raise HTTPException(status_code=404, detail="User not found")
