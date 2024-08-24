import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.base_routes import api_router
from db.base_class import Base
from db.session import engine
from dotenv import load_dotenv
import os

def include_router(app):
    app.include_router(api_router)

def create_tables(app):
    Base.metadata.create_all(bind=engine)


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

    include_router(app)
    create_tables(app)
    return app

load_dotenv(".env")
app = create_app()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
