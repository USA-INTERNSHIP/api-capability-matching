from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from db.models.user_model import Users
from db.models.admin_model import Admin
from schemas.admin_schema import AdminRegisterSchema

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
