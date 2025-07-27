from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import http_exception_handler
from typing import List
from sqlmodel import select
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings
from .deps import ChatMessageRepositoryDep, LLMRepositoryDep, SessionDep
from .models import ChatMessage, ChatRequest, HealthCheckResponse, Role
from .logger import logger
from .errors.llm_api_errors import LLMAPIUnauthorizedAccessError
from .errors.llm_api_errors import LLMAPIUnavailableError
from .errors.app_errors import TechnicalError

app = FastAPI(
    title="Turtle chat API",
    description="API for the Turtle chat app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().allowed_origins,
    allow_methods=["GET", "POST"],
)


@app.exception_handler(TechnicalError)
async def technical_error_handler(request: Request, exc: TechnicalError):
    logger.error(exc)
    raise HTTPException(status_code=500, detail=exc.message)


@app.exception_handler(LLMAPIUnauthorizedAccessError)
async def unauthorized_access_error_handler(
    request: Request, exc: LLMAPIUnauthorizedAccessError
):
    logger.error(exc)
    raise HTTPException(status_code=401, detail=exc.message)


@app.exception_handler(LLMAPIUnavailableError)
async def unavailable_error_handler(request: Request, exc: LLMAPIUnavailableError):
    logger.error(exc)
    raise HTTPException(status_code=502, detail=exc.message)


@app.get("/health", response_model=HealthCheckResponse)
def health_check():
    return HealthCheckResponse(status="ok")


@app.get("/chat", response_model=List[ChatMessage])
def get_chat_history(chat_message_repository: ChatMessageRepositoryDep):
    return chat_message_repository.get_all()


@app.post("/chat", response_model=ChatMessage)
def chat(
    llm_repository: LLMRepositoryDep,
    chat_message_repository: ChatMessageRepositoryDep,
    request: ChatRequest,
):
    user_message = ChatMessage.model_validate(request)
    chat_message_repository.create(user_message)

    messages = chat_message_repository.get_all()
    assistant_message = llm_repository.chat_completion(messages)
    chat_message_repository.create(assistant_message)

    return assistant_message
