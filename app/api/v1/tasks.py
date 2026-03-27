from fastapi import Depends, APIRouter, status
from app.schemas.task import TaskCreate, TaskCreateResponse, TaskUpdate
from app.dependencies import get_profile, get_db
from typing import Annotated
from app.schemas.user import UserInfo
from app.services.task_service import create_task as make_task, get_user_tasks, get_task_by_id as getTaskById, update_task_by_id, replace_task_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter()
db_dependency = Annotated[AsyncSession,Depends(get_db)]
profile_dependency = Annotated[UserInfo, Depends(get_profile)]

@router.post(
    '/',
    summary="Create a Task",
    response_description="This endpoint creates a task for the user",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskCreateResponse
)
async def create_task(user_task : TaskCreate,user : profile_dependency, db : db_dependency):
    result = await make_task(user_task, user, db)
    return result


@router.get(
    '/',
    summary="Get all User Tasks",
    response_description="Fetches all the Tasks of a logged in user",
    response_model=list[TaskCreateResponse]
)
async def get_tasks(user : profile_dependency, db : db_dependency):
    result = await get_user_tasks(user,db)
    return result


@router.get(
    '/{task_id}',
    summary="Get all User Tasks",
    response_description="Fetches all the Tasks of a logged in user",
    response_model=TaskCreateResponse,
    status_code=status.HTTP_200_OK
)
async def get_task_by_id(user : profile_dependency,task_id : UUID, db : db_dependency):
    result = await getTaskById(user,task_id,db)
    return result


@router.patch(
    '/{task_id}',
    summary="Update task with given id",
    description="Updates the Task with given Id and given Fields",
    response_model=TaskCreateResponse,
    status_code=status.HTTP_200_OK
)
async def update_task(update_task : TaskUpdate,task_id : UUID,db : db_dependency,user : profile_dependency):
    result = await update_task_by_id(update_task,task_id,db,user)
    return result


@router.put(
    '/{task_id}',
    summary="Replace Task Completely",
    response_description="Replaces all the Entries of a task with given id",
    status_code=status.HTTP_200_OK,
    response_model=TaskCreateResponse
)
async def replace_task(replaced_task : TaskCreate,task_id : UUID, db : db_dependency, user : profile_dependency):
    result = await replace_task_by_id(replaced_task,task_id,db,user)
    return result
