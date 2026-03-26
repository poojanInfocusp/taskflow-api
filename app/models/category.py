from uuid import uuid4, UUID
from datetime import datetime
from typing import Annotated

from sqlalchemy import func, ForeignKey, DateTime, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base import Base

uuid_pk = Annotated[UUID, mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)]
timestamp = Annotated[datetime, mapped_column(DateTime, server_default=func.now())]

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid_pk]
    
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, index=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    created_at: Mapped[timestamp]
