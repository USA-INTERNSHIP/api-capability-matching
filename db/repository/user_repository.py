from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.models.user_model import Users
from fastapi import HTTPException
from schemas.user_schema import UserSchema, UserRegisterSchema

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
        return user_obj
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

def get_users(db:Session):
    return db.query(Users).all()

def get_user_by_email(db:Session,email:str):
    return db.query(Users).filter(Users.email == email).first()