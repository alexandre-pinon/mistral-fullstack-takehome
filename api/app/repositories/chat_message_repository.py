from sqlmodel import Session, select

from ..models import ChatMessage
from ..errors import TechnicalError


class ChatMessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[ChatMessage]:
        try:
            return self.session.exec(select(ChatMessage)).all()
        except Exception as e:
            raise TechnicalError(message="Error getting chat messages", cause=e)

    def create(self, chat_message: ChatMessage):
        try:
            self.session.add(chat_message)
            self.session.commit()
            self.session.refresh(chat_message)
        except Exception as e:
            raise TechnicalError(message="Error creating chat message", cause=e)

        return chat_message
