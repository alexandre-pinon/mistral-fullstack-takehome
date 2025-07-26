from uuid import uuid4, UUID
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(SQLModel):
    id: UUID = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    role: Role
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(), index=True)


class ChatRequest(BaseModel):
    message: ChatMessage


class HealthCheckResponse(BaseModel):
    status: str
