from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

from db.models import Mentor
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
            username=admin.username.split('@')[0],  # Use the part before '@' as the username
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
