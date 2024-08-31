from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from db.repository.user_repository import pwd_context, get_user_by_email, create_user
from db.session import get_db

auth_routes = APIRouter()
load_dotenv(".env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password,user.password):
        return False
    return  user

def create_access_token(data: dict,expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('JWT_SECRETE_KEY'), algorithm=os.getenv('JWT_ALGORITHMS'))
    return encoded_jwt

@auth_routes.post("/login")
def login_for_access_token(user:UserRegisterSchema,db: Session = Depends(get_db)):
    user_db = authenticate_user(db,user.email,user.password)
    if not user_db:
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
    data = {"user":user_db.email}, expires_delta=access_token_expires
    )
        if not user_db:
            )
        access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        access_token = create_access_token(
            data={"user": user_db.email}, expires_delta=access_token_expires
        )

def verify_token(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRETE_KEY'), algorithms=[os.getenv('JWT_ALGORITHMS')])
        username: str = payload.get('user')
        if username is None:
            raise HTTPException(
                status_code=403, detail="Token is invalid or expired"
            )
        return  payload
    except JWTError:
        raise HTTPException(
            status_code=403, detail="Token is invalid or expired"
        )
@auth_routes.get("/verify-token/{token}")
async def verify_user_token(token: str):
    print(token)
    verify_token(token)
    return {"message" : "Token is valid"}