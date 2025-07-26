from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import uuid4

from .llm import LlmClientDep
from .config import get_settings


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


settings = get_settings()
app = FastAPI(
    title="Turtle chat API",
    description="API for the Turtle chat app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
)


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
def chat(
    request: ChatRequest,
    llm_client: LlmClientDep,
) -> ChatMessage:
    return ChatMessage(
        id=str(uuid4()),
        role=Role.ASSISTANT,
        content="Hello, how are you?",
        created_at=datetime.now(),
    )
