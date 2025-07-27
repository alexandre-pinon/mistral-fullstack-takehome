from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import api_router, health_router
from .errors import (
    TechnicalError,
    LLMAPIUnauthorizedAccessError,
    LLMAPIUnavailableError,
)
from .routers.handlers import (
    technical_error_handler,
    unauthorized_access_error_handler,
    unavailable_error_handler,
)

app = FastAPI(
    title="Turtle chat API",
    description="API for the Turtle chat app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().allowed_origins,
    allow_methods=["GET", "POST"],
)

app.include_router(api_router)
app.include_router(health_router)

app.add_exception_handler(TechnicalError, technical_error_handler)
app.add_exception_handler(
    LLMAPIUnauthorizedAccessError, unauthorized_access_error_handler
)
app.add_exception_handler(LLMAPIUnavailableError, unavailable_error_handler)
