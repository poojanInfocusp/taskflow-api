from app.db.session import AsyncSession, AsyncSessionLocal
from typing import AsyncGenerator

async def get_db()->AsyncGenerator[AsyncSession,None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise