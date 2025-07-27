from fastapi import HTTPException, Request

from ...errors import (
    TechnicalError,
    LLMAPIUnauthorizedAccessError,
    LLMAPIUnavailableError,
)
from ...config import logger


def technical_error_handler(request: Request, exc: TechnicalError):
    logger.error(exc)
    raise HTTPException(status_code=500, detail=exc.message)


def unauthorized_access_error_handler(
    request: Request, exc: LLMAPIUnauthorizedAccessError
):
    logger.error(exc)
    raise HTTPException(status_code=401, detail=exc.message)


def unavailable_error_handler(request: Request, exc: LLMAPIUnavailableError):
    logger.error(exc)
    raise HTTPException(status_code=502, detail=exc.message)
