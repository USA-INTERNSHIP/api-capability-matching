from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas.user_schema import UserSchema
from sqlalchemy.orm import Session
from db.repository.user_repository import create_user,get_users
from db.session import get_db


user_routes = APIRouter()

@user_routes.post("/user")
def create(user:UserSchema,db:Session = Depends(get_db)):
    try :
        user = create_user(user=user,db=db)
        return user
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
@user_routes.get("/user")
def get(db:Session=Depends(get_db)):
    try:
        user_list = get_users(db=db)
        if len(user_list) != 0:
            return user_list
        else :
            return JSONResponse(content="No details Found.",status_code=204)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

    