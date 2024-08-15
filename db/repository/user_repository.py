from sqlalchemy.orm import Session
from db.models.user_model import Users
from fastapi import HTTPException
from schemas.user_schema import UserSchema

def create_user(user:UserSchema,db:Session):
    
    user_obj = Users(
        email = user.email,
        password = user.password,
        firstName = user.firstName,
        middleName = user.middleName,
        lastName = user.lastName,
        mobile = user.mobile,
        gender = user.gender,
        highestQualification = user.highestQualification
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

def get_users(db:Session):
    return db.query(Users).all()