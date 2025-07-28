import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import delete
from app.models.sql_model import ChatMessage, Role
from tests.utils import assert_object_contains, assert_has_length


@pytest_asyncio.fixture(autouse=True)
async def cleanup(session: AsyncSession):
    """Cleanup the database after each test."""
    await session.exec(delete(ChatMessage))
    await session.commit()
    yield


@pytest.mark.asyncio
async def test_get_chat_history_endpoint_empty(
    client: AsyncClient, session: AsyncSession
):
    """Integration test for the get chat history endpoint."""
    # given

    # when
    response = await client.get("/api/v1/chat")

    # then
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_chat_history_endpoint_with_messages(
    client: AsyncClient, session: AsyncSession
):
    """Integration test for the get chat history endpoint."""
    # given
    message = ChatMessage(role=Role.USER, content="Hello, world!")
    session.add(message)
    await session.commit()

    # when
    response = await client.get("/api/v1/chat")

    # then
    data = response.json()
    assert response.status_code == 200
    assert_has_length(data, 1)
    assert_object_contains(data[0], message)
