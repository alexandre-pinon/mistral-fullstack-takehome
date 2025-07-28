import pytest_asyncio
from unittest.mock import AsyncMock
from typing import AsyncGenerator, List
from sqlmodel.ext.asyncio.session import AsyncSession
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.main import app
from app.config.settings import settings
from app.config.db import get_session
from app.repositories import LLMRepository
from app.models.sql_model import ChatMessage


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
async def mock_llm_repo() -> AsyncGenerator[LLMRepository, None]:
    """Mock the LLM repository."""
    mock_llm_repo = AsyncMock(spec=LLMRepository)

    async def mock_stream_generator(messages: List[ChatMessage]):
        yield "Mock response from AsyncMock"

    mock_llm_repo.chat_completion_stream.return_value = mock_stream_generator([])
    yield mock_llm_repo
    mock_llm_repo.reset_mock()


@pytest_asyncio.fixture
async def client(
    session: AsyncSession, mock_llm_repo: AsyncMock
) -> AsyncGenerator[AsyncClient, None]:
    """Test client fixture for FastAPI app."""

    async def override_get_session():
        yield session

    def override_llm_repo():
        return mock_llm_repo

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[LLMRepository] = override_llm_repo

    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
