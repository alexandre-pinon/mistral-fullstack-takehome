from typing import Annotated
from sqlmodel import Session
from fastapi import Depends

from ..config import get_session
from ..repositories import ChatMessageRepository, LLMRepository

SessionDep = Annotated[Session, Depends(get_session)]
LLMRepositoryDep = Annotated[LLMRepository, Depends()]


def get_chat_message_repository(session: SessionDep) -> ChatMessageRepository:
    return ChatMessageRepository(session)


ChatMessageRepositoryDep = Annotated[
    ChatMessageRepository, Depends(get_chat_message_repository)
]
