from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from ..config import get_session
from ..repositories import ChatMessageRepository, LLMRepository

AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
LLMRepositoryDep = Annotated[LLMRepository, Depends()]


def get_chat_message_repository(session: AsyncSessionDep) -> ChatMessageRepository:
    return ChatMessageRepository(session)


ChatMessageRepositoryDep = Annotated[
    ChatMessageRepository, Depends(get_chat_message_repository)
]
