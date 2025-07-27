from fastapi import HTTPException, Request

from ...errors.app_errors import TechnicalError
from ...errors.llm_api_errors import (
    LLMAPIUnauthorizedAccessError,
    LLMAPIUnavailableError,
)
from ...logger import logger


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
