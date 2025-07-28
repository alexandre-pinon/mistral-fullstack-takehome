import pytest_asyncio
from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.main import app
from app.config.settings import settings
from app.config.db import get_session


@pytest_asyncio.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database engine."""
    engine = create_async_engine(settings().database_url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for testing."""
    async with AsyncSession(test_engine) as session:
        yield session


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Test client fixture for FastAPI app."""

    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
