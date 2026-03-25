from sqlalchemy.ext.asyncio import (AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker)
from app.config import settings

engine : AsyncEngine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)