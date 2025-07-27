import json
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from fastapi.responses import StreamingResponse
from typing import List

from ..config import logger
from ..models import (
    UserMessageRequest,
    StreamChunkResponse,
    ChatMessage,
    Role,
    ChatMessagePublic,
)
from .deps import ChatMessageRepositoryDep, LLMRepositoryDep


chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.get("", response_model=List[ChatMessagePublic])
async def get_chat_history(
    chat_message_repository: ChatMessageRepositoryDep,
) -> List[ChatMessagePublic]:
    """Get all chat messages from the database."""
    return await chat_message_repository.get_all()


@chat_router.post("/messages", response_model=ChatMessagePublic)
async def send_user_message(
    chat_message_repository: ChatMessageRepositoryDep,
    body: UserMessageRequest,
) -> ChatMessagePublic:
    """
    Send a user message and store it in the database.
    Returns the created message with its ID for streaming.
    """
    user_message = ChatMessage(
        role=Role.USER,
        content=body.content,
    )

    return await chat_message_repository.create(user_message)


@chat_router.get("/messages/{message_id}/stream")
async def stream_assistant_response(
    message_id: str,
    llm_repository: LLMRepositoryDep,
    chat_message_repository: ChatMessageRepositoryDep,
):
    """
    Stream the assistant's response for a specific user message.
    The user message must exist in the database.
    """
    user_message = await chat_message_repository.get_by_id(message_id)
    if not user_message:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found",
        )

    if user_message.role != Role.USER:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Can only stream responses for user messages",
        )

    messages = await chat_message_repository.get_all()

    async def generate_stream() -> AsyncGenerator[str]:
        assistant_message = ChatMessage(
            role=Role.ASSISTANT,
            content="",
        )

        try:
            async for chunk in llm_repository.chat_completion_stream(messages):
                assistant_message.content += chunk
                yield f"data: {json.dumps(StreamChunkResponse(
                    done=False,
                    assistant_message=assistant_message.model_dump()
                ).model_dump(mode='json'))}\n\n"

            await chat_message_repository.create(assistant_message)

            yield f"data: {json.dumps(StreamChunkResponse(done=True).model_dump())}\n\n"

        except Exception as e:
            logger.error(f"Error in stream generation: {e}")
            error_response = StreamChunkResponse(
                done=True,
                error=f"Error: {str(e)}",
            )
            yield f"data: {json.dumps(error_response.model_dump())}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        },
    )
