from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessagePublic(BaseModel):
    id: UUID
    role: Role
    content: str
    created_at: datetime


class ChatRequestPayload(ChatMessagePublic): ...


class UserMessageRequest(BaseModel):
    content: str


class StreamChunkResponse(BaseModel):
    done: bool
    error: str | None = None
    assistant_message: ChatMessagePublic | None = None


class HealthCheckResponse(BaseModel):
    status: str
