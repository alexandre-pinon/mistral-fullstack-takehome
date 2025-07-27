import json
from fastapi import APIRouter, HTTPException, status
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
def get_chat_history(
    chat_message_repository: ChatMessageRepositoryDep,
) -> List[ChatMessagePublic]:
    """Get all chat messages from the database."""
    return chat_message_repository.get_all()


@chat_router.post("/messages", response_model=ChatMessagePublic)
def send_user_message(
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

    return chat_message_repository.create(user_message)


@chat_router.get("/messages/{message_id}/stream")
def stream_assistant_response(
    message_id: str,
    llm_repository: LLMRepositoryDep,
    chat_message_repository: ChatMessageRepositoryDep,
):
    """
    Stream the assistant's response for a specific user message.
    The user message must exist in the database.
    """
    user_message = chat_message_repository.get_by_id(message_id)
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found",
        )

    if user_message.role != Role.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only stream responses for user messages",
        )

    messages = chat_message_repository.get_all()

    def generate_stream():
        assistant_message = ChatMessage(
            role=Role.ASSISTANT,
            content="",
        )

        try:
            logger.info("Starting stream generation")
            for chunk in llm_repository.chat_completion_stream(messages):
                logger.info(f"Processing chunk: '{chunk}'")
                assistant_message.content += chunk
                yield f"data: {json.dumps(StreamChunkResponse(
                    done=False,
                    content=chunk
                ).model_dump())}\n\n"

            logger.info(
                f"Stream completed, final content: '{assistant_message.content}'"
            )
            chat_message_repository.create(assistant_message)

            yield f"data: {json.dumps(StreamChunkResponse(
                done=True,
                assistant_message=ChatMessagePublic.model_validate(assistant_message.model_dump()),
            ).model_dump(mode='json'))}\n\n"
            logger.info(f"End of stream")

        except Exception as e:
            logger.error(f"Error in stream generation: {e}", exc_info=True)
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


@chat_router.post("", response_model=ChatMessagePublic)
def chat_legacy(
    llm_repository: LLMRepositoryDep,
    chat_message_repository: ChatMessageRepositoryDep,
    body: UserMessageRequest,
) -> ChatMessagePublic:
    """
    Legacy endpoint that sends a message and returns the assistant response immediately.
    Use /messages for sending and /messages/{id}/stream for streaming instead.
    """
    user_message = ChatMessage(
        role=Role.USER,
        content=body.content,
    )
    chat_message_repository.create(user_message)

    messages = chat_message_repository.get_all()

    assistant_message = llm_repository.chat_completion(messages)
    chat_message_repository.create(assistant_message)

    return assistant_message
