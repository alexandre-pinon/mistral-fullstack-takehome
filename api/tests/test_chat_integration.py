import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import delete
from app.models.sql_model import ChatMessage, Role
from app.models import UserMessageRequest
from tests.utils import (
    assert_object_contains_model,
    assert_model_contains_model,
    assert_has_length,
    assert_object_contains_object,
)


@pytest_asyncio.fixture(autouse=True)
async def cleanup(session: AsyncSession):
    """Cleanup the database after each test."""
    await session.exec(delete(ChatMessage))
    await session.commit()
    yield


@pytest.mark.asyncio
async def test_get_chat_history_endpoint_empty(client: AsyncClient):
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
    assert_object_contains_model(data[0], message)


@pytest.mark.asyncio
async def test_send_user_message_endpoint(client: AsyncClient):
    """Integration test for the send user message endpoint."""
    # given
    body = UserMessageRequest(content="Hello, world!")

    # when
    response = await client.post("/api/v1/chat/messages", json=body.model_dump())

    # then
    assert response.status_code == 201
    assert_object_contains_object(response.json(), {"content": "Hello, world!"})


@pytest.mark.asyncio
async def test_stream_assistant_response_endpoint(
    client: AsyncClient, session: AsyncSession, mock_llm_repo: AsyncMock
):
    """Integration test for the stream assistant response endpoint."""
    # # given
    initial_context = [
        ChatMessage(role=Role.USER, content="Test message"),
        ChatMessage(role=Role.ASSISTANT, content="Test response"),
        ChatMessage(role=Role.USER, content="Test message 2"),
    ]
    last_message = initial_context[-1]
    session.add_all(initial_context)
    await session.commit()
    await session.refresh(last_message)

    # when
    chunks = []
    async with client.stream(
        "GET", f"/api/v1/chat/messages/{last_message.id}/stream"
    ) as response:
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream"

        async for chunk in response.aiter_text():
            if chunk.strip():
                chunks.append(chunk)

    # then
    mock_llm_repo.chat_completion_stream.assert_called_once()
    call_args = mock_llm_repo.chat_completion_stream.call_args
    messages_passed = call_args[0][0]

    assert_has_length(messages_passed, 3)
    assert_model_contains_model(messages_passed[0], initial_context[0])
    assert_model_contains_model(messages_passed[1], initial_context[1])
    assert_model_contains_model(messages_passed[2], initial_context[2])
    assert_has_length(chunks, 1)
    assert "Mock response from AsyncMock" in chunks[0]
