from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ..models import ChatMessage
from ..errors import TechnicalError


class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[ChatMessage]:
        try:
            results = await self.session.exec(select(ChatMessage))
            return results.all()
        except Exception as e:
            raise TechnicalError(message="Error getting chat messages", cause=e)

    async def get_by_id(self, message_id: str) -> ChatMessage | None:
        try:
            message_uuid = UUID(message_id)
            results = await self.session.exec(
                select(ChatMessage).where(ChatMessage.id == message_uuid).limit(1)
            )
            return results.first()
        except Exception as e:
            raise TechnicalError(message="Error getting chat message by ID", cause=e)

    async def create(self, chat_message: ChatMessage):
        try:
            self.session.add(chat_message)
            await self.session.commit()
            await self.session.refresh(chat_message)
        except Exception as e:
            raise TechnicalError(message="Error creating chat message", cause=e)

        return chat_message
