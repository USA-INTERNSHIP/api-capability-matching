from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routes.base_routes import api_router
from db.base_class import Base
from db.session import engine


def include_router(app):
    app.include_router(api_router)


def create_tables(app):
    Base.metadata.create_all(bind=engine)


def create_app():
    app = FastAPI(title=settings.PROJECT_NAME)

    # CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this to specific origins if needed
        allow_credentials=True,
        allow_methods=["*"],  # Change this to specific methods if needed
        allow_headers=["*"],  # Change this to specific headers if needed
    )

    include_router(app)
    create_tables(app)
    return app


app = create_app()
