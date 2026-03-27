from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import StrEnum
from datetime import datetime
from uuid import UUID

class Role(StrEnum):
    user = "user"
    admin = "admin"


# Registration Request-Response Validation Models
class UserCreate(BaseModel):
    email : EmailStr
    password: str = Field(max_length=255,min_length=5)
    full_name : str = Field(max_length=255)
    role : Role = Field(default=Role.user)
    is_active : bool = Field(default=True)


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: UUID
    email : EmailStr
    full_name : str
    role : Role
    is_active: bool
    created_at : datetime
    updated_at : datetime | None = None


# Login Request-Response Validation Models
class UserLoginRquest(BaseModel):
    email : EmailStr
    password : str


class UserSchemaLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : UUID
    email: EmailStr
    full_name : str
    role : Role
    is_active : bool


class UserLoginResponse(BaseModel):
    access_token : str
    token_type : str
    user : UserSchemaLogin

# Access Token payload Generation Schema
class Payload(BaseModel):
    sub : UUID
    email : EmailStr
    exp: datetime
    type : str
    role : Role

class UserInfo(BaseModel):
    id : UUID
    email : EmailStr
    role : Role