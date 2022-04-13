from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    email: Optional[str] = Field(alias="user_email")
    user_id: int = Field(alias="user_id")
    name: str = Field(alias="user_name")
    phone_number: Optional[str]
    domain_name: Optional[str]
