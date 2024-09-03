from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas.user_schema import UserRegisterSchema
from sqlalchemy.orm import Session
from db.repository.user_repository import create_user,get_users, get_user_by_email
from db.session import get_db


user_routes = APIRouter()

@user_routes.post("/register")
def create(user:UserRegisterSchema,db:Session = Depends(get_db)):
    try :
        if get_user_by_email(db,user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        user = create_user(user=user,db=db)
        return user
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
@user_routes.get("/user")
def get(db:Session=Depends(get_db)):
    try:
        return get_users(db=db)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

    