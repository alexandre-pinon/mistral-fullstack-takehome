from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from uuid import uuid4

from .models import ChatMessage, ChatRequest, HealthCheckResponse, Role
from .llm import LlmClientDep
from .config import get_settings


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
