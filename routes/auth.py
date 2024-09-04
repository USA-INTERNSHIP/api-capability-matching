import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import  OAuth2PasswordBearer
from fastapi.security import OAuth2AuthorizationCodeBearer
import requests as http_requests
from google.auth.transport import requests
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from google.oauth2 import id_token
from sqlalchemy.orm import Session
from db.repository.user_repository import pwd_context, get_user_by_email, create_user
from db.session import get_db
from schemas.google_auth_schema import GoogleAuthRequest
from schemas.user_schema import UserRegisterSchema, UserLoginSchema

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
def login_for_access_token(user:UserLoginSchema,db: Session = Depends(get_db)):
    user_db = authenticate_user(db,user.email,user.password)
    if not user_db:
        raise HTTPException(
        status_code=401,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
    data = {"user":user_db.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token,"user":{"username":user_db.username,"email":user_db.email,"userRole":user_db.userRole}}


def exchange_access_token_for_id_token(access_token):
    response = http_requests.get(
        'https://oauth2.googleapis.com/tokeninfo',
        params={'access_token': access_token}
    )
    if response.status_code != 200:
        raise ValueError('Invalid access token')
    token_info = response.json()
    return token_info
@auth_routes.post("/verify-google-token")
async def verify_google_token(auth_request: GoogleAuthRequest ,db: Session = Depends(get_db)):
    try:
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        try:
            res = id_token.verify_oauth2_token(auth_request.token, requests.Request(), CLIENT_ID)
        except ValueError:
            res = exchange_access_token_for_id_token(auth_request.token)

        user_mail = res['email']
        if user_mail != auth_request.user_details.get('email'):
            raise ValueError("User email doesn't match")

        user_db = get_user_by_email(db=db,email=user_mail)
        if not user_db:
            new_user =  UserRegisterSchema(
            username = user_mail,
            email= user_mail,
            password = secrets.token_urlsafe(32),
            socialLogin= True,
             userRole = auth_request.user_details.get('userRole')
            )
            user_db = create_user(new_user,db=db)
        access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        access_token = create_access_token(
            data={"user": user_db.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "user": {"username": user_db.username, "email": user_db.email, "userRole": user_db.userRole}}

    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Invalid token ={str(e)}")

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