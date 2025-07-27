from typing import AsyncGenerator
from functools import lru_cache
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from .settings import settings


@lru_cache
def engine() -> Engine:
    return create_async_engine(settings().database_url)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine()) as session:
        yield session
