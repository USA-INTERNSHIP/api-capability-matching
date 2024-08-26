from pydantic import BaseModel, Field


class UserRegisterSchema(BaseModel):
    username: str = Field()
    email: str = Field(min_length=3)
    password: str = Field()
    socialLogin: bool = Field()
    userRole: str = Field()

class UserSchema(UserRegisterSchema):
    firstName:str = Field(min_length=1)
    middleName:str = Field(min_length=1)
    lastName:str = Field(min_length=1)

    mobile:int  = Field(min_digits=10 )
    gender:str = Field(min_length=4)
    highestQualification:str = Field(min_length=1)