from fastapi import Depends, APIRouter
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.user import UserCreate

router = APIRouter()

# Reusable Dependencies
type db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post('auth/register')
async def register_user(user: UserCreate,db : db_dependency):
    pass