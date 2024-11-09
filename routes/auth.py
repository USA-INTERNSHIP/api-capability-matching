import asyncio
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
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
from functools import wraps
from typing import List

auth_routes = APIRouter()
load_dotenv(".env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRETE_KEY'), algorithms=[os.getenv('JWT_ALGORITHMS')])
        username: str = payload.get('user')
        role: str = payload.get('user_role')  # Added role check
        if username is None or role is None:  # Added role check
            raise HTTPException(
                status_code=403, detail="Token is invalid or expired"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=403, detail="Token is invalid or expired"
        )


def check_roles(allowed_roles: List[str]):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, current_user: dict = Depends(verify_token), **kwargs):
            user_role = current_user.get('user_role')
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail="You don't have sufficient permissions to perform this action"
                )
            if asyncio.iscoroutinefunction(func):
                return await func(*args, current_user=current_user, **kwargs)
            return func(*args, current_user=current_user, **kwargs)
        return async_wrapper
    return decorator


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('JWT_SECRETE_KEY'), algorithm=os.getenv('JWT_ALGORITHMS'))
    return encoded_jwt


@auth_routes.post("/login")
async def login_for_access_token(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = authenticate_user(db, user.email, user.password)
    if not user_db:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={
            "user": user_db.email,
            "user_id": user_db.id,
            "username": user_db.username,
            "user_role": user_db.userRole
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token}


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
async def verify_google_token(auth_request: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        try:
            res = id_token.verify_oauth2_token(auth_request.token, requests.Request(), CLIENT_ID)
        except ValueError:
            res = exchange_access_token_for_id_token(auth_request.token)

        user_mail = res['email']
        if user_mail != auth_request.user_details.get('email'):
            raise ValueError("User email doesn't match")

        user_db = get_user_by_email(db=db, email=user_mail)
        if user_db:

            if user_db.userRole != auth_request.user_details.get('userRole'):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid role.",
                    headers={"WWW-Authenticate": "Bearer"}
                )
        if not user_db:
            new_user = UserRegisterSchema(
                username=user_mail,
                email=user_mail,
                password=secrets.token_urlsafe(32),
                socialLogin=True,
                userRole=auth_request.user_details.get('userRole')
            )
            user_db = create_user(new_user, db=db)

        access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
        access_token = create_access_token(
            data={
                "user": user_db.email,
                "user_id": user_db.id,
                "username": user_db.username,
                "user_role": user_db.userRole
            },
            expires_delta=access_token_expires
        )
        return {"access_token": access_token}

    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Invalid token ={str(e)}")


@auth_routes.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token)
    return {"message": "Token is valid"}