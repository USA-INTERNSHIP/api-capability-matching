from fastapi import APIRouter
from routes.user_routes import user_routes
from routes.auth import auth_routes
api_router = APIRouter()

api_router.include_router(user_routes)
api_router.include_router(auth_routes)