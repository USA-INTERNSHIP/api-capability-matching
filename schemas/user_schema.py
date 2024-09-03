from pydantic import BaseModel, Field


class UserRegisterSchema(BaseModel):
    username: str = Field()
    email: str = Field(min_length=3)
    password: str = Field()
    socialLogin: bool = Field()
    userRole: str = Field()

