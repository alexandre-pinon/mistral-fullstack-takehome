from fastapi import APIRouter

from ..config import settings
from .chat_router import chat_router

api_router = APIRouter(prefix=settings().api_prefix)

api_router.include_router(chat_router)
