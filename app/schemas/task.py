from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum
from uuid import UUID

class TaskStatus(StrEnum):
    todo="todo"
    in_progress="in_progress"
    done="done"

class TaskPriority(StrEnum):
    low="low"
    medium="medium"
    high="high"

class TaskCreate(BaseModel):
    title : str
    description : str | None = None
    status : TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date : datetime | None = None
    category_id : UUID | None = None

class TaskCreateResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id : UUID
    title : str
    description : str | None = None
    status : TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date : datetime | None = None
    category_id : UUID | None = None
    created_at : datetime
    updated_at : datetime
