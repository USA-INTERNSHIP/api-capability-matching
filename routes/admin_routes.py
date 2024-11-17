from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.repository.admin_repository import create_admin  # Call to the repository method
from db.session import get_db
from schemas.admin_schema import AdminRegisterSchema

# Initialize the router
admin_routes = APIRouter()


# Route for creating an admin user
@admin_routes.post("/create-admin")
def create_admin_route(admin: AdminRegisterSchema, db: Session = Depends(get_db)):
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
