from sys import prefix

from fastapi import APIRouter

from routes.hiring_manager_routes import hiring_manager_routes
from routes.mentor_routes import mentor_routes
from routes.user_routes import user_routes
from routes.auth import auth_routes
from routes.intern_routes import intern_routes  # Import the intern routes
from routes.admin_routes import admin_routes

api_router = APIRouter()

# Include user and authentication routes
api_router.include_router(user_routes)
api_router.include_router(auth_routes, prefix='/auth', tags=["auth"])


api_router.include_router(admin_routes, prefix="/admin", tags=["admin"])

# Routes for hiring manager
api_router.include_router(hiring_manager_routes, prefix="/hiring-manager", tags=["hiring-manager"])

# Routes for interns
api_router.include_router(intern_routes, prefix="/intern", tags=["intern"])

#Routes for mentor
api_router.include_router(mentor_routes,prefix="/mentor", tags=["mentor"])