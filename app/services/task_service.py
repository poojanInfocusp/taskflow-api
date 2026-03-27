from app.schemas.task import TaskCreate
from app.schemas.user import UserInfo
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

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