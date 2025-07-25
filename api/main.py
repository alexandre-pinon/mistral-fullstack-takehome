from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import uuid4

app = FastAPI()


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    id: str
    role: Role
    content: str
    created_at: datetime


class ChatRequest(BaseModel):
    message: ChatMessage


class HealthCheckResponse(BaseModel):
    status: str


@app.get("/health")
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")


@app.get("/chat")
def get_chat_history() -> List[ChatMessage]:
    return [
        {
            "id": str(uuid4()),
            "role": Role.USER,
            "content": "Hello, how are you?",
            "created_at": datetime.now(),
        }
    ]


@app.post("/chat")
def chat(request: ChatRequest) -> ChatMessage:
    return ChatMessage(
        id=str(uuid4()),
        role=Role.ASSISTANT,
        content="Hello, how are you?",
        created_at=datetime.now(),
    )
