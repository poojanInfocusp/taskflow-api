from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from datetime import datetime
from uuid import UUID

class Role(str,Enum):
    user = "user"
    admin = "admin"


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
