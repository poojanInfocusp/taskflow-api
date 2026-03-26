from app.db.session import AsyncSession, AsyncSessionLocal
from typing import AsyncGenerator
from fastapi import HTTPException

async def get_db()->AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        try:
            print("DB Connection has Established")
            yield session
        except HTTPException:
            raise
        except Exception:
            await session.rollback()
            raise
