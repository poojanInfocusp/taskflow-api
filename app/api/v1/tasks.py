from fastapi import Depends, APIRouter, status
from app.schemas.task import TaskCreate, TaskCreateResponse
from app.dependencies import get_profile, get_db
from typing import Annotated
from app.schemas.user import UserInfo
from app.services.task_service import create_task as make_task
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
db_dependency = Annotated[AsyncSession,Depends(get_db)]


@router.post(
    '/',
    summary="Create a Task",
    response_description="This endpoint creates a task for the user",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskCreateResponse
)
async def create_task(user_task : TaskCreate,user : Annotated[UserInfo,Depends(get_profile)], db : db_dependency):
    result = await make_task(user_task, user, db)
    return result