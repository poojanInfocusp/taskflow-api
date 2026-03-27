from app.schemas.task import TaskCreate, TaskCreateResponse, TaskUpdate
from app.schemas.user import UserInfo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, Update, CursorResult, update
from app.models.task import Task
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError
from uuid import UUID

async def create_task(user_task : TaskCreate, user : UserInfo, db : AsyncSession)->Task:
    try:
        task_obj = Task(**user_task.model_dump(),owner_id=user.id)
        # Add the task_obj in the session
        db.add(task_obj)
        # commit the task_obj to the database
        await db.commit()
        # Refresh the task_obj
        await db.refresh(task_obj)
        return task_obj
    except IntegrityError as i:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Integrity Error Occured'
        )
    except DataError as i:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Data Error Occured'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occured in the database"
        )
    
async def get_user_tasks(user : UserInfo, db : AsyncSession)->list[TaskCreateResponse]:
    try:
        query = await db.execute(Select(Task).where(Task.owner_id==user.id))
        userTasks = query.scalars().all()
        
        result = [TaskCreateResponse.model_validate(userTasks[i]) for i in range(len(userTasks))]
        
        return result
    except Exception as we:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error Occured"
        )

async def get_task_by_id(user : UserInfo,taskId : UUID, db : AsyncSession)->TaskCreateResponse | None:
    try:
        query = await db.execute(Select(Task).where(Task.owner_id==user.id,Task.id==taskId))
        userTasks = query.scalars().first()

        if userTasks is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task with the given ID does not exist !"
            )
        
        result = TaskCreateResponse.model_validate(userTasks)
        
        return result
    except HTTPException:
        raise
    except Exception as we:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error Occured"
        )


async def update_task_by_id(update_task : TaskUpdate, task_id : UUID, db : AsyncSession, user : UserInfo)->TaskCreateResponse:
    try:
        result = await db.execute(Select(Task).where(Task.owner_id==user.id,Task.id==task_id))
        
        user_task = result.scalars().first()

        if user_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task with Given ID Not Found'
            )
        
        user_task_dict =TaskCreateResponse.model_validate(user_task).model_dump()
        updated_task_dict = update_task.model_dump(exclude_unset=True)

        for key in updated_task_dict:
            user_task_dict[key] = updated_task_dict[key]

        query = await db.execute(Update(Task).where(Task.owner_id==user.id,Task.id==task_id).values(**user_task_dict))

        await db.commit()
        await db.refresh(user_task)
        return TaskCreateResponse.model_validate(user_task)
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Integrity error while updating task"
        )
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task data provided"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected database error occurred while updating task"
        )


async def replace_task_by_id(replaced_task : TaskCreate,task_id : UUID, db : AsyncSession, user : UserInfo):
    try:
        rep_task = replaced_task.model_dump()
        result = await db.execute(Update(Task).where(Task.owner_id==user.id,Task.id==task_id).values(**rep_task).returning(Task.id))

        updated_id = result.scalars().first()

        if updated_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        await db.commit()

        task = (
            await db.execute(Select(Task).where(Task.id == updated_id))
        ).scalars().first()

        return TaskCreateResponse.model_validate(task)
    except Exception:
        raise 
