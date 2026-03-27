from uuid import uuid4, UUID
from datetime import datetime
from typing import Annotated

from sqlalchemy import func, VARCHAR, DateTime, Enum, ForeignKey  # Added ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # SQLAlchemy's DB type
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

uuid_pk = Annotated[
    UUID, 
    mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
]
timestamp = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid_pk]
    title: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    
    # Use str | None for the type; SQLAlchemy handles the 'Null' part
    description: Mapped[str | None] = mapped_column(VARCHAR(1000), nullable=True)
    
    status: Mapped[str] = mapped_column(
        Enum('todo', 'in_progress', 'done', name="task_status"), 
        default='todo', 
        server_default='todo' # Good for DB-level defaults
    )
    
    priority: Mapped[str] = mapped_column(
        Enum('low', 'medium', 'high', name="task_priority"), 
        default='medium', 
        server_default='medium'
    )
    
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    category_id: Mapped[UUID | None] = mapped_column(ForeignKey("categories.id"), nullable=True)

    created_at: Mapped[timestamp] 
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
