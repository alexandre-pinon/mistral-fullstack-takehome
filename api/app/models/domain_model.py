from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatRequestPayload(BaseModel):
    id: UUID
    role: Role
    content: str
    created_at: datetime


class HealthCheckResponse(BaseModel):
    status: str
