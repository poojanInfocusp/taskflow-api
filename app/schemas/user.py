from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class Role(str,Enum):
    user = "user"
    admin = "admin"


class UserCreate(BaseModel):
    email : EmailStr
    password: str = Field(max_length=255)
    full_name : str = Field(max_length=255)
    role : Role = Field(default=Role.user)
    is_active : bool = Field(default=True)
