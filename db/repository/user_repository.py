from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.models.hiring_manager_model import HiringManager
from db.models.user_model import Users
from fastapi import HTTPException
from schemas.user_schema import UserRegisterSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user:UserRegisterSchema,db:Session):
    try:
        hashed_password = pwd_context.hash(user.password if user.password else None)
        user_obj = Users(
            email = user.email,
            password = hashed_password,
            username = user.username.split('@')[0],
            socialLogin = user.socialLogin,
            userRole = user.userRole,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        try:
            if user_obj.userRole == "HIRING_MANAGER":
                hiring_manager = HiringManager(
                    user_id = user_obj.id
                )
                print("HiringManager created: ", hiring_manager.id)
                db.add(hiring_manager)
                db.commit()
                db.refresh(hiring_manager)
            db.commit()
            db.refresh(user_obj)
        except Exception as ie:
            db.rollback()
            db.delete(user_obj)
            db.commit()
            raise HTTPException(status_code=400, detail=f"HiringManager creation failed: {str(e)}")

        return user_obj
    except Exception as e:
        db.rollback()
        return HTTPException(status_code=400, detail=str(e))

def get_users(db:Session):
    return db.query(Users).all()

def get_user_by_email(db:Session,email:str):
    return db.query(Users).filter(Users.email == email).first()

def get_userid_by_email(db:Session,email:str) -> int:
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return user.id
    else:
        raise HTTPException(status_code=404, detail="User not found")