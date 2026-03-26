from fastapi import Depends, APIRouter, status
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from typing import Annotated
from app.services import auth_service

# Dependency
db_dependency = Annotated[AsyncSession,Depends(get_db)]

router = APIRouter()


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Register a new User",
    response_description="The newly created user's public profile"
)
async def register_user(user_data : UserCreate, db : db_dependency):
    result = await auth_service.create_user(user_data=user_data,db=db)
    return result

