from pydantic import BaseModel, Field


class GoogleAuthRequest(BaseModel):
    token: str = Field()
    user_details: dict = Field()