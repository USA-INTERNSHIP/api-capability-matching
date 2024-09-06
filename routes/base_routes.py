from fastapi import APIRouter

from routes.hiring_manager_routes import hiring_manager_routes
from routes.user_routes import user_routes
from routes.auth import auth_routes
api_router = APIRouter()

api_router.include_router(user_routes)
api_router.include_router(auth_routes,prefix='/auth')

# Routes for hiring manager
api_router.include_router(hiring_manager_routes,prefix="/hiring-manager")

