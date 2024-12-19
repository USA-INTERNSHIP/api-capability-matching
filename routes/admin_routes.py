from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.repository.admin_repository import create_admin, create_mentor  # Call to the repository method
from db.repository.user_repository import get_user_by_email, create_user
from db.session import get_db
from routes.auth import check_roles, verify_token
from schemas.admin_schema import AdminRegisterSchema
from schemas.user_schema import UserRegisterSchema

# Initialize the router
admin_routes = APIRouter()


# Route for creating an admin user
@admin_routes.post("/create-admin")
@check_roles(["ADMIN"])
def create_admin_route(admin: AdminRegisterSchema,current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        # Call the repository function to create the admin user
        admin_user = create_admin(admin=admin, db=db)
        # Return a success response
        return {
            "message": "Admin user created successfully",
            "user": {
                "username": admin_user.username,
                "email": admin_user.email,
                "role": admin_user.userRole,
                "id": admin_user.id
            }
        }
    except Exception as e:
        # Return error response if exception occurs
        raise HTTPException(status_code=400, detail=str(e))

@admin_routes.post("/register-mentor")
@check_roles(["ADMIN"])
def create(user: UserRegisterSchema,current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        # Check if the email is already registered
        if get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create the user
        created_user = create_mentor(user=user, db=db)

        # Prepare the response to match the required format
        response_user = {
            "username": created_user.username,
            "email": created_user.email,
            "socialLogin": created_user.socialLogin,
            "password": created_user.password,  # Ensure this is hashed in your database
            "id": created_user.id,
            "userRole": created_user.userRole
        }

        return {
            "user": response_user,
            "status": "success",
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

