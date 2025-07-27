from fastapi import APIRouter
from typing import List

from ..models import ChatMessage, ChatRequest
from ..deps import ChatMessageRepositoryDep, LLMRepositoryDep


chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.get("", response_model=List[ChatMessage])
def get_chat_history(chat_message_repository: ChatMessageRepositoryDep):
    return chat_message_repository.get_all()


@chat_router.post("", response_model=ChatMessage)
def chat(
    llm_repository: LLMRepositoryDep,
    chat_message_repository: ChatMessageRepositoryDep,
    request: ChatRequest,
) -> ChatMessage:
    user_message = ChatMessage.model_validate(request)
    chat_message_repository.create(user_message)

    messages = chat_message_repository.get_all()
    assistant_message = llm_repository.chat_completion(messages)
    chat_message_repository.create(assistant_message)

    return assistant_message
