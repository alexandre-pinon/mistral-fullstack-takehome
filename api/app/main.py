from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from uuid import uuid4
from sqlmodel import select

# from .llm import LlmClientDep
from .config import settings
from .deps import SessionDep
from .models import ChatMessage, ChatRequest, HealthCheckResponse, Role


app = FastAPI(
    title="Turtle chat API",
    description="API for the Turtle chat app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().allowed_origins,
    allow_methods=["GET", "POST"],
)


@app.get("/health", response_model=HealthCheckResponse)
def health_check():
    return HealthCheckResponse(status="ok")


@app.get("/chat", response_model=List[ChatMessage])
def get_chat_history(session: SessionDep):
    return session.exec(select(ChatMessage)).all()


@app.post("/chat", response_model=ChatMessage)
def chat(
    # llm_client: LlmClientDep,
    session: SessionDep,
    request: ChatRequest,
):
    user_message = ChatMessage.model_validate(request)
    session.add(user_message)
    session.commit()

    # assistant_message = llm_client.generate_message(user_message)
    # session.add(assistant_message)
    # session.commit()
    # session.refresh(assistant_message)
    return ChatMessage.model_construct(
        role=Role.ASSISTANT, content="Hello, how are you?"
    )
