from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    email:str = Field(min_length=3)
    password:str = Field(min_length=8,max_length=16)
    firstName:str = Field(min_length=1)
    middleName:str = Field(min_length=1)
    lastName:str = Field(min_length=1)
    mobile:int  = Field(min_digits=10 )
    gender:str = Field(min_length=4)
    highestQualification:str = Field(min_length=1)