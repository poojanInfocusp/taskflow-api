from sqlalchemy.ext.asyncio import (AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.config import settings

engine : AsyncEngine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,
    max_overflow=10,
    pool_pre_ping=True
)

AsyncSessionLocale = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db()->AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocale() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
    
class Base(DeclarativeBase):
    pass