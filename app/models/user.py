from uuid import uuid4, UUID
from datetime import datetime
from typing import Annotated

from sqlalchemy import func, VARCHAR, Enum, BOOLEAN, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # SQLAlchemy's DB type
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

# Using Annotated to create reusable types (DRY - Don't Repeat Yourself)
uuid_pk = Annotated[UUID, mapped_column(PG_UUID(as_uuid=True),primary_key=True, default=uuid4)]
timestamp = Annotated[datetime, mapped_column(DateTime, server_default=func.now())]

class User(Base):
    __tablename__ = "users"

    # ID: Fixed as_uuid=True to match Mapped[UUID]
    id: Mapped[uuid_pk]
    
    # Email: Added index=True as requested
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True, nullable=False)
    
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(VARCHAR(512), nullable=True)
    
    full_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    
    # Role: Defined the Enum properly
    role: Mapped[str] = mapped_column(
        Enum("user", "admin", name="user_role"), 
        default="user", 
        server_default="user"
    )
    
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True, server_default="true")
    
    # Timestamps: Using func.now() for database-level timing
    created_at: Mapped[timestamp]
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now()  # This handles the "edit it" logic automatically
    )
