from pydantic import BaseModel

class AdminRegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    socialLogin: bool
    userRole: str

    class Config:
        orm_mode = True  # Ensure compatibility with SQLAlchemy models
