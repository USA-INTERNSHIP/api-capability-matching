from pydantic import BaseModel, Field

class AdminRegisterSchema(BaseModel):
    username: str = Field()
    email: str = Field(min_length=3)
    password: str = Field()
    socialLogin: bool = Field()
    userRole: str = Field()

    # class Config:
    #     orm_mode = True  # Ensure compatibility with SQLAlchemy models
