from fastapi import Depends, APIRouter, status, Response
from app.schemas.user import UserCreate, UserResponse, UserLoginRquest, UserLoginResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from typing import Annotated
from app.services.auth_service import create_user, login as loginUser

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
    print("Creating My User and it's working fine for some reason")
    result = await create_user(user_data=user_data,db=db)
    return result


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=UserLoginResponse,
    summary="Login User",
    response_description="Returns User details and Access token in the body",
)
async def login(user : UserLoginRquest, db : db_dependency , response : Response):
    result = await loginUser(user,db,response)
    return result
