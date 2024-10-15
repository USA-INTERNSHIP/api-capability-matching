from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas.user_schema import UserRegisterSchema
from sqlalchemy.orm import Session
from db.repository.user_repository import create_user,get_users, get_user_by_email
from db.session import get_db


user_routes = APIRouter()

@user_routes.post("/register")
def create(user: UserRegisterSchema, db: Session = Depends(get_db)):
    try:
        # Check if the email is already registered
        if get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create the user
        created_user = create_user(user=user, db=db)

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

@user_routes.get("/user")
def get(db: Session = Depends(get_db)):
    try:
        users = get_users(db=db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    