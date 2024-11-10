import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.base_class import Base
from db.models import Job, Mentor, Intern, HiringManager, MentorApplications, InternApplications
from db.models.user_model import Users
from db.session import engine
from routes.base_routes import api_router


def include_router(app):
    app.include_router(api_router)


def create_tables(app):
    tables = [
        Base.metadata.tables[table_name] for table_name in [
            "users",
            "hiringmanager",
            "intern",
            "mentor",
            "job",
            "mentor_applications",
            "intern_applications"
        ]
    ]
    Base.metadata.create_all(bind=engine, tables=tables)

def create_app():
    app = FastAPI(title=os.getenv("PROJECT_NAME"))

    # CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this to specific origins if needed
        allow_credentials=True,
        allow_methods=["*"],  # Change this to specific methods if needed
        allow_headers=["*"],  # Change this to specific headers if needed
    )
    @app.get("/health-check")
    def health_check():
        return {"status": "ok"}
    include_router(app)
    create_tables(app)
    return app


load_dotenv(".env")
app = create_app()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
