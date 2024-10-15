from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.models.hiring_manager_model import HiringManager
from db.models.intern_model import Intern
from db.models.user_model import Users
from fastapi import HTTPException
from schemas.user_schema import UserRegisterSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user: UserRegisterSchema, db: Session):
    try:
        hashed_password = pwd_context.hash(user.password if user.password else None)
        user_obj = Users(
            email=user.email,
            password=hashed_password,
            username=user.username.split('@')[0],
            socialLogin=user.socialLogin,
            userRole=user.userRole,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)

        # Logic for hiring manager role
        if user_obj.userRole == "HIRING_MANAGER":
            hiring_manager = HiringManager(
                user_id=user_obj.id
            )
            db.add(hiring_manager)
            db.commit()
            db.refresh(hiring_manager)

        # Logic for intern role
        if user_obj.userRole == "INTERN":
            intern = Intern(
                user_id=user_obj.id
            )
            db.add(intern)
            db.commit()
            db.refresh(intern)

        return user_obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


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